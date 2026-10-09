/* Assistant de révision PolyWE (S25) : chat IA payé par le compte OpenRouter de chaque visiteur.
   JavaScript natif, sans dépendance ni étape de build ; le générateur l’inclut sur toutes les pages.
   Sécurité : la clé du visiteur vit dans localStorage. Aucune réponse du modèle n’est donc insérée comme HTML :
   elle est analysée en un petit arbre (gras, italique, listes, code, liens http(s)), puis construite nœud par nœud. */
(function () {
  "use strict";

  // ——— Réglages ———
  // Domaines où le modèle peut faire sa recherche web (outil openrouter:web_search, moteur Exa) : liste à adapter.
  const ALLOWED_DOMAINS = ["iiwelding.org", "twi-global.com", "iso.org", "afnor.org", "aws.org", "inrs.fr"];

  // Modèles proposés. Au chargement, seuls ceux qu’OpenRouter publie et qui acceptent les outils (tool calling) sont gardés.
  // `ids` : identifiants exacts, par ordre de préférence ; `match` : repère une variante dont l’identifiant n’est pas encore connu.
  const MODEL_CANDIDATES = [
    {label: "Claude Opus 5.5", ids: ["anthropic/claude-opus-5.5"]},
    {label: "GPT-6.1 Sol", ids: ["openai/gpt-6.1-sol"]},
    {label: "Gemini 4 Argon", ids: ["google/gemini-4-argon"], match: /gemini[\s-]*4\b.*argon/i},
    {label: "Kimi K3", ids: ["moonshotai/kimi-k3"]},
    {label: "Mistral Large 4", ids: ["mistralai/mistral-large-4-0", "mistralai/mistral-large-4"]},
    {label: "DeepSeek V4 Pro", ids: ["deepseek/deepseek-v4-pro", "deepseek/deepseek-v4-pro-0813"], match: /deepseek.*v4.*pro/i},
  ];
  const DEFAULT_MODEL = "openai/gpt-6.1-sol";

  const SYSTEM_PROMPT = `Tu es l'assistant de révision IWE de PolyWE (Polytech Nantes, DU Ingénierie du soudage).
1. Réponds à partir des EXTRAITS fournis. Cite chaque affirmation avec l'identifiant entre crochets, ex. [RDM-04].
2. Si les EXTRAITS ne couvrent pas la question :
   - notion générale et stable : réponds avec tes connaissances, en commençant par « Hors cours : » ;
   - fait précis (valeur, exigence ou numéro de norme, donnée produit, date) : fais UNE recherche web et cite l'URL. Si tu ne trouves pas de source fiable, dis que tu ne sais pas.
   - Ne cherche jamais sur le web si les extraits suffisent.
3. En cas de doute, dis-le. N'invente ni valeur numérique, ni norme, ni source.
4. 120 mots maximum, sauf calcul (formule, application numérique, unité, résultat).
5. Hors soudage et matériaux : décline en une phrase.`;

  const API = "https://openrouter.ai/api/v1";
  const AUTH = "https://openrouter.ai/auth";
  const STORE = "polywe_chat_"; // l’origine pemcode.github.io est partagée par tous les dépôts du compte
  const MAX_TOKENS = 1500;
  const HISTORY_EXCHANGES = 3;
  const SECTIONS_SENT = 3;
  const EXTRACT_CHARS = 1500;

  // ——— PKCE ———
  function base64url(bytes) {
    let binary = "";
    for (const byte of bytes) binary += String.fromCharCode(byte);
    return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  const createVerifier = (cryptoImpl = globalThis.crypto) => base64url(cryptoImpl.getRandomValues(new Uint8Array(32)));
  async function codeChallenge(verifier, cryptoImpl = globalThis.crypto) {
    return base64url(new Uint8Array(await cryptoImpl.subtle.digest("SHA-256", new TextEncoder().encode(verifier))));
  }
  function authorizeUrl(callback, challenge) {
    const url = new URL(AUTH);
    url.searchParams.set("callback_url", callback);
    url.searchParams.set("code_challenge", challenge);
    url.searchParams.set("code_challenge_method", "S256");
    return url.href;
  }
  // OpenRouter ajoute ?code= à l’adresse de retour : on lui donne la page courante sans ancre ni ancien code.
  function callbackUrl(href) {
    const url = new URL(href);
    url.searchParams.delete("code");
    url.hash = "";
    return url.href;
  }

  // ——— Choix des extraits : mêmes normalisations que la recherche du wiki, classement BM25 ———
  const normalize = text => String(text).toLowerCase().normalize("NFD")
    .replace(/\p{M}/gu, "")
    .replace(/t\s*8\s*\/?\s*5/g, "t85")
    .replace(/[σετγν]/g, char => ({"σ": " sigma ", "ε": " epsilon ", "τ": " tau ", "γ": " gamma ", "ν": " nu "})[char]);
  const STOPWORDS = new Set(("a au aux avec ce ces cet cette c ca cela d dans de des du elle elles en est et etre il ils j je l la le les leur leurs lui m "
    + "ma me mes moi mon n ne nous on ou par pas plus pour qu que quel quelle quelles quels qui quoi s sa se ses son sont sur t ta te tes toi ton tu un une "
    + "vos votre vous y comment pourquoi quand combien explique expliquer peux peut faut fait donne cours entre comme alors ainsi aussi tres bien sans sous ici "
    + "avant apres lors pendant depuis").split(" "));
  const SUFFIXES = ["ement", "ation", "age", "ure", "euse", "eur", "ee", "er", "e"];
  function stem(word) {
    if (word.length > 4 && /[sx]$/.test(word)) word = word.slice(0, -1);
    const suffix = SUFFIXES.find(end => word.endsWith(end) && word.length - end.length >= 4);
    return suffix ? word.slice(0, -suffix.length) : word;
  }
  const terms = text => normalize(text).split(/[^\p{L}\p{N}]+/u)
    .filter(word => word && (word.length > 1 || /\d/.test(word)) && !STOPWORDS.has(word)).map(stem);
  const decode = value => { try { return decodeURIComponent(value); } catch { return value; } };
  const pathOf = url => decode(String(url).split("#")[0]);

  const prepared = new WeakMap();
  function prepare(rows) {
    if (prepared.has(rows)) return prepared.get(rows);
    const docs = rows.map(row => {
      const counts = new Map();
      const add = (text, weight) => { for (const term of terms(text || "")) counts.set(term, (counts.get(term) || 0) + weight); };
      add(row.titre, 3);
      add(row.texte, 1);
      let length = 0;
      for (const count of counts.values()) length += count;
      // Titre et mots-clés du cours départagent les sections, sans suffire à en retenir une.
      return {row, counts, length, course: new Set(terms(`${row.cours || ""} ${(row.mots_cles || []).join(" ")}`))};
    });
    const df = new Map();
    for (const doc of docs) for (const term of doc.counts.keys()) df.set(term, (df.get(term) || 0) + 1);
    const result = {docs, df, average: docs.reduce((sum, doc) => sum + doc.length, 0) / (docs.length || 1)};
    prepared.set(rows, result);
    return result;
  }

  // Sections du site entier ; la page courante n’a qu’un léger avantage. Une section doit contenir au moins
  // deux mots de la question (un seul si la question n’en compte qu’un ou deux) : une question hors sujet n’envoie rien.
  function rankSections(rows, question, {page = "", limit = SECTIONS_SENT} = {}) {
    const query = [...new Set(terms(question))];
    if (!query.length || !rows || !rows.length) return [];
    const {docs, df, average} = prepare(rows);
    const needed = Math.min(2, Math.ceil(query.length / 2));
    const scored = [];
    for (const doc of docs) {
      let score = 0, matched = 0, course = 0;
      for (const term of query) {
        if (doc.course.has(term)) course++;
        const tf = doc.counts.get(term);
        if (!tf) continue;
        const n = df.get(term);
        matched++;
        score += Math.log(1 + (docs.length - n + 0.5) / (n + 0.5)) * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * doc.length / average));
      }
      if (matched < needed) continue;
      score *= 1 + 0.15 * course;
      if (/^avant de commencer/i.test(doc.row.titre)) score *= 0.7; // rappel et plan du cours : utile, mais après le fond
      scored.push({row: doc.row, score: page && pathOf(doc.row.url) === page ? score * 1.15 : score});
    }
    scored.sort((a, b) => b.score - a.score || a.row.id.localeCompare(b.row.id));
    const best = scored.length ? scored[0].score : 0;
    return scored.filter(item => item.score >= best * 0.35).slice(0, limit);
  }

  const clip = (text, max) => text.length <= max ? text : text.slice(0, max - 1).trimEnd() + "…";

  // Le passage le plus riche en termes de la question, élargi à ses voisins dans la limite de caractères.
  function bestPassage(text, queryTerms, max = EXTRACT_CHARS) {
    text = String(text || "");
    if (text.length <= max) return text;
    const wanted = new Set(queryTerms);
    const lines = text.split("\n");
    const scores = lines.map(line => new Set(terms(line).filter(term => wanted.has(term))).size);
    let best = 0;
    scores.forEach((score, index) => { if (score > scores[best]) best = index; });
    const budget = max - 4;
    if (lines[best].length >= budget) return clip(lines[best], max);
    let start = best, end = best, size = lines[best].length;
    for (let grew = true; grew;) {
      grew = false;
      if (end + 1 < lines.length && size + 1 + lines[end + 1].length <= budget) { size += 1 + lines[++end].length; grew = true; }
      if (start > 0 && size + 1 + lines[start - 1].length <= budget) { size += 1 + lines[--start].length; grew = true; }
    }
    return (start > 0 ? "…\n" : "") + lines.slice(start, end + 1).join("\n") + (end < lines.length - 1 ? "\n…" : "");
  }

  // Le texte sélectionné passe en premier, puis les sections les plus pertinentes, sans doublon.
  function buildExtracts({rows = [], question = "", selection = null, page = ""}) {
    const extracts = [];
    const selected = selection && String(selection.text || "").trim();
    if (selected) {
      extracts.push({id: selection.id || "TEXTE-SELECTIONNE", titre: selection.titre ? `Texte sélectionné · ${selection.titre}` : "Texte sélectionné sur la page",
                     cours: selection.cours || "", url: selection.url || "", texte: clip(selected, EXTRACT_CHARS)});
    }
    const wording = selected ? `${question}\n${selected}` : question;
    const queryTerms = terms(wording);
    for (const {row} of rankSections(rows, wording, {page, limit: SECTIONS_SENT + 1})) {
      if (extracts.length >= SECTIONS_SENT + (selected ? 1 : 0)) break;
      if (extracts.some(item => item.id === row.id)) continue;
      extracts.push({id: row.id, titre: row.titre, cours: row.cours, url: row.url, texte: bestPassage(row.texte, queryTerms)});
    }
    return extracts;
  }

  // ——— Requête ———
  function userMessage(question, extracts, verify) {
    const blocks = extracts.length
      ? extracts.map(item => `[${item.id}] ${[item.cours, item.titre].filter(Boolean).join(" — ")}\n${item.texte}`).join("\n\n")
      : "Aucun extrait des cours ne correspond à cette question.";
    let text = `EXTRAITS\n${blocks}\n\nQUESTION\n${question}`;
    if (verify) text += "\n\nCONSIGNE\nFais UNE recherche web pour répondre à cette question et cite l’URL de chaque source utilisée. Si tu ne trouves pas de source fiable, dis que tu ne sais pas.";
    return text;
  }

  // Les extraits ne sont joints qu’à la dernière question : l’historique garde les questions et réponses seules.
  function buildRequest({model, question, extracts = [], history = [], verify = false}) {
    const previous = history.filter(item => item && item.answer && !item.error).slice(-HISTORY_EXCHANGES);
    return {
      model,
      messages: [
        {role: "system", content: SYSTEM_PROMPT},
        ...previous.flatMap(item => [{role: "user", content: item.question}, {role: "assistant", content: item.answer}]),
        {role: "user", content: userMessage(question, extracts, verify)},
      ],
      stream: true,
      max_tokens: MAX_TOKENS,
      reasoning: {effort: "low"},
      tools: [{type: "openrouter:web_search", parameters: {engine: "exa", max_uses: 1, max_results: 3, max_characters: 1500, allowed_domains: ALLOWED_DOMAINS}}],
      usage: {include: true}, // usage (tokens, coût) renvoyé dans le dernier morceau du flux
    };
  }

  // ——— Lecture de la réponse ———
  const ID = "[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+";
  const CITE = new RegExp(`\\[(${ID}(?:\\s*[,;]\\s*${ID})*)\\](?!\\()`, "g");
  const splitIds = group => group.split(/\s*[,;]\s*/).map(id => id.toUpperCase());
  function citations(text) {
    const ids = [];
    for (const match of String(text).matchAll(CITE)) for (const id of splitIds(match[1])) if (!ids.includes(id)) ids.push(id);
    return ids;
  }
  // Un identifiant est vérifié seulement s’il figurait dans les extraits envoyés avec la question.
  function checkCitation(id, sent, known) {
    const row = known.get(id);
    return {id, verified: sent.has(id), url: row && row.url ? row.url : null};
  }

  function safeUrl(value) {
    try {
      const url = new URL(String(value).trim());
      return url.protocol === "https:" || url.protocol === "http:" ? url.href : null;
    } catch {
      return null;
    }
  }

  const INLINE = new RegExp([
    "`([^`\\n]+)`",
    "\\[([^\\]\\n]+)\\]\\(([^()\\s]*(?:\\([^()\\s]*\\)[^()\\s]*)*)\\)",
    `\\[(${ID}(?:\\s*[,;]\\s*${ID})*)\\]`,
    "\\*\\*(?=\\S)([^\\n]*?\\S)\\*\\*",
    "__(?=\\S)([^\\n]*?\\S)__",
    "\\*(?=[^\\s*])([^*\\n]*?[^\\s*])?\\*",
    "(https?:\\/\\/[^\\s<>\"'()\\[\\]]*[^\\s<>\"'()\\[\\].,;:!?»])",
  ].join("|"), "gi");

  function parseInline(text) {
    const nodes = [];
    let last = 0;
    for (const match of text.matchAll(INLINE)) {
      if (match.index > last) nodes.push({type: "text", text: text.slice(last, match.index)});
      const [raw, code, label, href, cite, strong, strong2, em, bare] = match;
      if (code !== undefined) nodes.push({type: "code", text: code});
      else if (label !== undefined) {
        const url = safeUrl(href);
        nodes.push(url ? {type: "link", href: url, children: [{type: "text", text: label}]} : {type: "text", text: raw});
      } else if (cite !== undefined) nodes.push({type: "cite", ids: splitIds(cite)});
      else if (strong !== undefined || strong2 !== undefined) nodes.push({type: "strong", children: parseInline(strong ?? strong2)});
      else if (bare !== undefined) {
        const url = safeUrl(bare);
        nodes.push(url ? {type: "link", href: url, children: [{type: "text", text: bare}]} : {type: "text", text: bare});
      } else nodes.push({type: "em", children: parseInline(em ?? raw.slice(1, -1))});
      last = match.index + raw.length;
    }
    if (last < text.length) nodes.push({type: "text", text: text.slice(last)});
    return nodes;
  }

  // Markdown minimal : paragraphes, titres rendus en gras, listes, blocs de code. Tout le reste reste du texte.
  function parseMarkdown(text) {
    const lines = String(text).replace(/\r\n?/g, "\n").split("\n");
    const blocks = [];
    let paragraph = null, list = null;
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const fence = line.match(/^\s*(```|~~~)/);
      if (fence) {
        const body = [];
        for (i++; i < lines.length && !lines[i].trim().startsWith(fence[1]); i++) body.push(lines[i]);
        blocks.push({type: "pre", text: body.join("\n")});
        paragraph = list = null;
        continue;
      }
      if (!line.trim() || /^\s{0,3}([-*_])(\s*\1){2,}\s*$/.test(line)) { paragraph = list = null; continue; }
      const heading = line.match(/^\s{0,3}#{1,6}\s+(.*)$/);
      if (heading) { blocks.push({type: "h", inline: parseInline(heading[1].trim())}); paragraph = list = null; continue; }
      const item = line.match(/^\s*(?:([-*+•])|(\d{1,3})[.)])\s+(.*)$/);
      if (item) {
        const ordered = item[2] !== undefined;
        if (!list || list.ordered !== ordered) {
          list = {type: "list", ordered, start: ordered ? Number(item[2]) : 1, items: []};
          blocks.push(list);
          paragraph = null;
        }
        list.items.push(parseInline(item[3].trim()));
        continue;
      }
      if (list && /^\s+\S/.test(line)) { list.items[list.items.length - 1].push({type: "br"}, ...parseInline(line.trim())); continue; }
      list = null;
      if (paragraph) paragraph.inline.push({type: "br"}, ...parseInline(line.trim()));
      else blocks.push(paragraph = {type: "p", inline: parseInline(line.trim())});
    }
    return blocks;
  }

  // Flux SSE : morceaux coupés n’importe où, commentaires « : OPENROUTER PROCESSING », fin « [DONE] ».
  function createStreamParser(onEvent) {
    let buffer = "";
    const handle = line => {
      if (!line.startsWith("data:")) return;
      const data = line.slice(5).trim();
      if (!data) return;
      if (data === "[DONE]") { onEvent({done: true}); return; }
      try { onEvent(JSON.parse(data)); } catch { /* ligne incomplète ou étrangère : ignorée */ }
    };
    return {
      push(text) {
        buffer += text;
        for (let end = buffer.indexOf("\n"); end >= 0; end = buffer.indexOf("\n")) {
          handle(buffer.slice(0, end).replace(/\r$/, ""));
          buffer = buffer.slice(end + 1);
        }
      },
      end() { if (buffer) handle(buffer.replace(/\r$/, "")); buffer = ""; },
    };
  }

  const emptyAnswer = () => ({text: "", sources: [], usage: null, finish: null, error: null});
  function reduceChunk(state, chunk) {
    const next = {...state, sources: [...state.sources]};
    if (!chunk || typeof chunk !== "object") return next;
    if (chunk.error) next.error = chunk.error;
    if (chunk.usage) next.usage = chunk.usage;
    for (const choice of chunk.choices || []) {
      const delta = choice.delta || choice.message || {};
      if (typeof delta.content === "string") next.text += delta.content;
      for (const note of delta.annotations || []) {
        const cite = note && note.type === "url_citation" ? note.url_citation || note : null;
        const url = cite && safeUrl(cite.url);
        if (url && !next.sources.some(source => source.url === url)) next.sources.push({url, title: String(cite.title || "").trim() || new URL(url).hostname});
      }
      if (choice.finish_reason) next.finish = choice.finish_reason;
      if (choice.error) next.error = choice.error;
    }
    return next;
  }

  function errorFor(status, payload) {
    const detail = payload && payload.error && typeof payload.error.message === "string" ? payload.error.message.trim() : "";
    const tail = detail ? ` (${detail})` : "";
    const messages = {
      0: "Connexion à OpenRouter impossible. Vérifiez votre connexion internet, puis réessayez.",
      400: `Requête refusée par OpenRouter${tail}.`,
      401: "Votre connexion OpenRouter n’est plus valide (clé expirée ou révoquée). Reconnectez-vous.",
      402: "Crédits OpenRouter insuffisants pour cette question. Ajoutez des crédits sur openrouter.ai ou choisissez un modèle moins coûteux.",
      403: `Question refusée par la modération du fournisseur du modèle${tail}.`,
      404: "Ce modèle n’est pas disponible chez OpenRouter pour le moment. Choisissez-en un autre.",
      408: "Le modèle a mis trop de temps à répondre. Réessayez.",
      429: "Trop de requêtes en peu de temps (limite d’OpenRouter ou du fournisseur). Patientez quelques secondes, puis réessayez.",
      502: "Le fournisseur du modèle est indisponible ou surchargé. Réessayez dans un instant ou choisissez un autre modèle.",
      503: "Le fournisseur du modèle est indisponible ou surchargé. Réessayez dans un instant ou choisissez un autre modèle.",
    };
    return {message: messages[status] || `Erreur OpenRouter ${status}${tail}. Réessayez.`, reconnect: status === 401};
  }

  const isOffCourse = text => /^hors cours\s*[*_]*\s*:/i.test(String(text).replace(/^[\s*_#>«"“]+/, ""));

  function pickModels(candidates, api) {
    const usable = (Array.isArray(api) ? api : []).filter(model => model && typeof model.id === "string" && !model.id.includes(":")
      && Array.isArray(model.supported_parameters) && model.supported_parameters.includes("tools"));
    const ids = new Set(usable.map(model => model.id));
    const models = [];
    for (const candidate of candidates) {
      let id = candidate.ids.find(known => ids.has(known));
      if (!id && candidate.match) {
        id = usable.filter(model => candidate.match.test(model.id) || candidate.match.test(model.name || "")).map(model => model.id)
          .sort((a, b) => a.length - b.length || a.localeCompare(b))[0];
      }
      if (id) models.push({label: candidate.label, id});
    }
    return models;
  }

  function formatUsage(usage) {
    if (!usage) return "";
    const number = new Intl.NumberFormat("fr-FR");
    const sent = usage.prompt_tokens, generated = usage.completion_tokens;
    let text = `${number.format(usage.total_tokens ?? (sent || 0) + (generated || 0))} tokens`;
    if (sent != null && generated != null) text += ` (${number.format(sent)} envoyés, ${number.format(generated)} générés)`;
    if (typeof usage.cost === "number") text += ` · ${usage.cost.toLocaleString("fr-FR", {maximumSignificantDigits: 2})} $`;
    return text;
  }

  const core = {ALLOWED_DOMAINS, MODEL_CANDIDATES, DEFAULT_MODEL, SYSTEM_PROMPT, createVerifier, codeChallenge, authorizeUrl, callbackUrl,
    terms, rankSections, bestPassage, buildExtracts, buildRequest, citations, checkCitation, parseMarkdown, createStreamParser,
    emptyAnswer, reduceChunk, errorFor, isOffCourse, pickModels, formatUsage};
  if (typeof window === "undefined") {
    if (typeof module === "object" && module.exports) module.exports = core;
    return;
  }

  // ——— Interface ———
  const script = document.getElementById("wiki-chat");
  if (!script || !script.src || document.getElementById("polywe-chat")) return;
  const assets = new URL("./", script.src);
  const siteRoot = new URL("../", assets);
  let page = decode(location.pathname).slice(decode(siteRoot.pathname).length);
  if (!page || page.endsWith("/")) page += "index.html";

  const storage = area => ({
    get(name) { try { return window[area].getItem(STORE + name); } catch { return null; } },
    set(name, value) { try { window[area].setItem(STORE + name, value); } catch { /* stockage indisponible */ } },
    remove(name) { try { window[area].removeItem(STORE + name); } catch { /* stockage indisponible */ } },
  });
  const local = storage("localStorage"), session = storage("sessionStorage");
  const readJSON = (area, name) => { try { return JSON.parse(area.get(name) || "null"); } catch { return null; } };

  let key = local.get("key");
  let model = local.get("model") || DEFAULT_MODEL;
  let models = null, modelsVerified = false, modelsPromise = null;
  let conversation = (readJSON(session, "conversation") || [])
    .filter(entry => entry && typeof entry.question === "string" && typeof entry.answer === "string" && !entry.pending)
    .map(entry => ({...entry, sent: Array.isArray(entry.sent) ? entry.sent : [], sources: Array.isArray(entry.sources) ? entry.sources : []}));
  let selection = null, captured = null, busy = false, controller = null;
  let known = new Map();
  const views = new Map();

  function el(tag, props = {}, ...children) {
    const node = document.createElement(tag);
    for (const [name, value] of Object.entries(props)) {
      if (value == null || value === false) continue;
      if (name.startsWith("on")) node.addEventListener(name.slice(2), value);
      else node.setAttribute(name === "className" ? "class" : name, value === true ? "" : value);
    }
    node.append(...children.flat(Infinity).filter(child => child != null && child !== false));
    return node;
  }
  function icon(...paths) {
    const ns = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(ns, "svg");
    for (const [name, value] of Object.entries({viewBox: "0 0 24 24", width: "20", height: "20", fill: "none", stroke: "currentColor",
      "stroke-width": "1.8", "stroke-linecap": "round", "stroke-linejoin": "round", "aria-hidden": "true", focusable: "false"})) svg.setAttribute(name, value);
    for (const d of paths) { const path = document.createElementNS(ns, "path"); path.setAttribute("d", d); svg.append(path); }
    return svg;
  }

  const host = document.createElement("div");
  host.id = "polywe-chat";
  host.setAttribute("style", "all:initial!important;display:none!important");
  const shadow = host.attachShadow({mode: "open"});
  const styles = el("link", {rel: "stylesheet", href: new URL("chat-widget.css", assets).href});
  styles.addEventListener("load", () => { host.setAttribute("style", "all:initial!important"); place(); });

  const launcher = el("button", {type: "button", className: "launcher", "aria-controls": "pwc-panel", "aria-expanded": "false", "aria-haspopup": "dialog",
    title: "Assistant de révision (IA)"}, icon("M5 5.5h14a1.5 1.5 0 0 1 1.5 1.5v8.5A1.5 1.5 0 0 1 19 17h-8l-4.5 3.5V17H5a1.5 1.5 0 0 1-1.5-1.5V7A1.5 1.5 0 0 1 5 5.5z", "M8 10h8M8 13h5"),
    el("span", {}, "Chat"));
  const closeButton = el("button", {type: "button", className: "icon-button", "aria-label": "Fermer le chat", title: "Fermer (Échap)"}, icon("m6 6 12 12M18 6 6 18"));
  const select = el("select", {id: "pwc-model"});
  const newButton = el("button", {type: "button", className: "link-button"}, "Nouvelle conversation");
  const logoutButton = el("button", {type: "button", className: "link-button"}, "Se déconnecter");
  const bar = el("div", {className: "bar"}, el("label", {for: "pwc-model"}, "Modèle"), select, newButton, logoutButton);
  const log = el("div", {className: "log", role: "log", "aria-live": "polite", "aria-label": "Conversation", tabindex: "0"});
  const loginButton = el("button", {type: "button", className: "primary"}, "Se connecter avec OpenRouter");
  const login = el("div", {className: "login"},
    el("p", {}, "Posez vos questions sur les cours : l’assistant répond à partir des sections du wiki et cite ses sources."),
    el("p", {}, "Il utilise ", el("strong", {}, "votre propre compte OpenRouter"), " : chaque question est facturée sur votre compte, selon le modèle choisi."),
    loginButton,
    el("p", {className: "small"}, "La clé créée reste dans ce navigateur. Conseil : fixez-lui une limite de crédit dans les réglages de votre compte OpenRouter."));
  const status = el("p", {className: "status", role: "status"});
  const chipText = el("q", {className: "chip-text"});
  const chipRemove = el("button", {type: "button", className: "icon-button small", "aria-label": "Retirer le texte sélectionné", title: "Retirer"}, icon("m6 6 12 12M18 6 6 18"));
  const chip = el("div", {className: "chip", hidden: true}, el("span", {className: "chip-label"}, "Texte sélectionné, envoyé en priorité :"), chipText, chipRemove);
  const question = el("textarea", {id: "pwc-question", rows: "2", maxlength: "2000", placeholder: "Votre question sur le soudage ou les matériaux…"});
  const sendButton = el("button", {type: "submit", className: "primary"}, "Envoyer");
  const stopButton = el("button", {type: "button", className: "secondary", hidden: true}, "Arrêter");
  const composer = el("form", {className: "composer"}, el("label", {for: "pwc-question", className: "sr"}, "Votre question"), question,
    el("div", {className: "actions"}, el("span", {className: "small"}, "Entrée pour envoyer, Maj+Entrée pour aller à la ligne"), stopButton, sendButton));
  const panel = el("section", {id: "pwc-panel", className: "panel", role: "dialog", "aria-labelledby": "pwc-title", hidden: true},
    el("header", {className: "head"}, el("div", {}, el("h2", {id: "pwc-title"}, "Assistant de révision"), el("p", {className: "sub"}, "IA · avec votre compte OpenRouter")), closeButton),
    bar, log, login, status, chip, composer,
    el("p", {className: "notice"}, "Vos questions, le texte sélectionné et des extraits des cours sont envoyés à OpenRouter et au fournisseur du modèle, et facturés sur votre compte OpenRouter."));
  shadow.append(styles, launcher, panel);
  document.body.append(host);

  // ——— Ouverture, fermeture, placement ———
  const narrow = matchMedia("(max-width: 640px)");
  function place() {
    // Sur téléphone, le bouton « Menu » du wiki occupe déjà le coin : le chat se place juste au-dessus.
    const menu = document.querySelector(".wiki-menu-button");
    let bottom = 16;
    if (menu && getComputedStyle(menu).display !== "none") {
      const box = menu.getBoundingClientRect();
      if (box.height) bottom = Math.max(bottom, Math.round(innerHeight - box.top + 10));
    }
    launcher.style.bottom = `${bottom}px`;
    panel.setAttribute("aria-modal", String(narrow.matches));
  }
  addEventListener("resize", place);

  function open({focus = true} = {}) {
    panel.hidden = false;
    launcher.hidden = true;
    launcher.setAttribute("aria-expanded", "true");
    place();
    render();
    if (key) loadModels();
    log.scrollTop = log.scrollHeight;
    if (focus) (key ? question : loginButton).focus();
  }
  function close() {
    panel.hidden = true;
    launcher.hidden = false;
    launcher.setAttribute("aria-expanded", "false");
    launcher.focus();
  }

  function readSelection() {
    const current = document.getSelection();
    if (!current || current.isCollapsed || !current.rangeCount) return null;
    let node = current.getRangeAt(0).commonAncestorContainer;
    if (node && node.nodeType !== 1) node = node.parentElement;
    if (!node || node === host || host.contains(node)) return null;
    const text = current.toString().replace(/[ \t ]+/g, " ").replace(/\s*\n\s*/g, "\n").trim();
    if (text.length < 3) return null;
    const anchors = [];
    for (let item = node; item && item !== document.body; item = item.parentElement) if (item.id) anchors.push(item.id);
    return {text: text.slice(0, 4000), anchors};
  }
  // Le passage sélectionné garde l’identifiant de sa section quand elle est connue.
  function resolveSelection(rows) {
    if (!selection) return null;
    const here = new Map(rows.filter(row => pathOf(row.url) === page).map(row => [decode(row.url.split("#")[1] || ""), row]));
    const row = selection.anchors.map(anchor => here.get(anchor)).find(Boolean);
    return row ? {id: row.id, titre: row.titre, cours: row.cours, url: row.url, text: selection.text} : {text: selection.text};
  }

  launcher.addEventListener("pointerdown", () => { captured = readSelection(); });
  launcher.addEventListener("click", () => {
    const picked = captured || readSelection();
    captured = null;
    if (picked) selection = picked;
    open();
  });
  closeButton.addEventListener("click", close);
  chipRemove.addEventListener("click", () => { selection = null; render(); question.focus(); });
  document.addEventListener("keydown", event => {
    if (event.key !== "Escape" || panel.hidden || event.defaultPrevented) return;
    if (document.documentElement.classList.contains("wiki-tiroir")) return; // le tiroir du wiki se ferme d’abord
    event.preventDefault();
    close();
  });
  panel.addEventListener("keydown", event => {
    if (event.key !== "Tab" || !narrow.matches) return;
    const items = [...panel.querySelectorAll("button, a[href], select, textarea, summary, [tabindex='0']")].filter(item => item.getClientRects().length);
    if (!items.length) return;
    const first = items[0], last = items[items.length - 1], active = shadow.activeElement;
    if (event.shiftKey && active === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && active === last) { event.preventDefault(); first.focus(); }
  });

  // ——— Connexion OAuth PKCE ———
  async function startLogin() {
    loginButton.disabled = true;
    try {
      const verifier = createVerifier();
      const challenge = await codeChallenge(verifier);
      local.set("pkce", JSON.stringify({verifier, hash: location.hash, t: Date.now()}));
      location.assign(authorizeUrl(callbackUrl(location.href), challenge));
    } catch {
      loginButton.disabled = false;
      status.textContent = "Connexion impossible depuis ce navigateur (chiffrement indisponible).";
    }
  }
  // Un ?code= n’est échangé que si une connexion a été lancée ici : un lien forgé reste sans effet.
  async function finishLogin() {
    const url = new URL(location.href);
    const code = url.searchParams.get("code");
    const pending = readJSON(local, "pkce");
    if (!code || !pending || typeof pending.verifier !== "string") return;
    local.remove("pkce");
    if (Date.now() - pending.t > 15 * 60 * 1000) return;
    url.searchParams.delete("code");
    url.hash = pending.hash || "";
    window.history.replaceState(window.history.state, "", url.href);
    if (url.hash) document.getElementById(decode(url.hash.slice(1)))?.scrollIntoView();
    open({focus: false});
    status.textContent = "Connexion à OpenRouter…";
    try {
      const response = await fetch(`${API}/auth/keys`, {method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code, code_verifier: pending.verifier, code_challenge_method: "S256"})});
      const data = await response.json().catch(() => ({}));
      if (!response.ok || typeof data.key !== "string" || !data.key) throw new Error(String(response.status));
      key = data.key;
      local.set("key", key);
      status.textContent = "Connecté à OpenRouter. Posez votre question.";
      loadModels();
    } catch {
      status.textContent = "La connexion à OpenRouter a échoué. Réessayez.";
    }
    render();
    (key ? question : loginButton).focus();
  }
  loginButton.addEventListener("click", startLogin);
  logoutButton.addEventListener("click", () => {
    key = null;
    local.remove("key");
    controller?.abort();
    status.textContent = "Déconnecté. La clé reste valable chez OpenRouter tant que vous ne la supprimez pas dans les réglages de votre compte (Keys).";
    render();
    loginButton.focus();
  });

  // ——— Modèles ———
  function loadModels() {
    modelsPromise ||= (async () => {
      const cached = readJSON(local, "models");
      let list = cached && Date.now() - cached.t < 864e5 && Array.isArray(cached.list) && cached.list.length ? cached.list : null;
      if (!list) {
        try {
          const response = await fetch(`${API}/models`);
          if (response.ok) list = pickModels(MODEL_CANDIDATES, (await response.json()).data);
          if (list && list.length) local.set("models", JSON.stringify({t: Date.now(), list}));
          else list = null;
        } catch { list = null; }
      }
      modelsVerified = Boolean(list);
      models = list || MODEL_CANDIDATES.map(candidate => ({label: candidate.label, id: candidate.ids[0]}));
      if (!models.some(item => item.id === model)) model = models.some(item => item.id === DEFAULT_MODEL) ? DEFAULT_MODEL : models[0].id;
      select.replaceChildren(...models.map(item => el("option", {value: item.id}, item.label)));
      select.value = model;
      select.title = modelsVerified ? "" : "Liste non vérifiée : OpenRouter n’a pas pu être interrogé.";
    })();
    return modelsPromise;
  }
  select.addEventListener("change", () => { model = select.value; local.set("model", model); });

  // ——— Extraits des cours ———
  let rowsPromise = null;
  const loadRows = () => rowsPromise ||= fetch(new URL("chat-extraits.json", assets)).then(response => {
    if (!response.ok) throw new Error("Extraits indisponibles");
    return response.json();
  }).then(rows => {
    known = new Map(rows.map(row => [row.id, row]));
    return rows;
  }).catch(error => { rowsPromise = null; throw error; });
  question.addEventListener("focus", () => { loadRows().catch(() => {}); }, {once: true});

  // ——— Rendu sûr des messages ———
  const external = (href, children) => el("a", {href, target: "_blank", rel: "noopener noreferrer nofollow"}, children);
  function citeView(ids, sent, sources) {
    const span = el("span", {className: "cite"}, "[");
    const badge = () => el("span", {className: "unverified", title: "Cet identifiant ne figurait pas dans les extraits envoyés"}, "source non vérifiée");
    const checks = ids.map(id => checkCitation(id, sent, sources));
    checks.forEach((check, index) => {
      if (index) span.append(", ");
      span.append(check.url ? el("a", {href: new URL(check.url, siteRoot).href, title: sources.get(check.id)?.titre || null, "data-cite": check.id}, check.id)
        : el("span", {}, check.id));
      if (!check.verified && checks.length > 1) span.append(" ", badge());
    });
    span.append("]");
    if (checks.length === 1 && !checks[0].verified) span.append(" ", badge());
    return span;
  }
  function inline(nodes, sent, sources) {
    return nodes.map(node => {
      if (node.type === "text") return document.createTextNode(node.text);
      if (node.type === "br") return el("br");
      if (node.type === "code") return el("code", {}, node.text);
      if (node.type === "strong") return el("strong", {}, inline(node.children, sent, sources));
      if (node.type === "em") return el("em", {}, inline(node.children, sent, sources));
      if (node.type === "link") return external(node.href, inline(node.children, sent, sources));
      return citeView(node.ids, sent, sources);
    });
  }
  function block(item, sent, sources) {
    if (item.type === "pre") return el("pre", {}, el("code", {}, item.text));
    if (item.type === "list") {
      return el(item.ordered ? "ol" : "ul", {start: item.ordered && item.start > 1 ? String(item.start) : null},
        item.items.map(entry => el("li", {}, inline(entry, sent, sources))));
    }
    if (item.type === "h") return el("p", {className: "heading"}, el("strong", {}, inline(item.inline, sent, sources)));
    return el("p", {}, inline(item.inline, sent, sources));
  }

  function answerView(entry) {
    const sent = new Set(entry.sent.map(item => item.id));
    const sources = new Map([...known, ...entry.sent.filter(item => item.url).map(item => [item.id, item])]);
    const offCourse = isOffCourse(entry.answer);
    const box = el("div", {className: "answer"});
    if (offCourse) box.append(el("p", {className: "badge"}, "Hors cours"));
    const body = el("div", {className: "md"}, parseMarkdown(entry.answer).map(item => block(item, sent, sources)));
    if (!entry.answer && entry.pending) body.append(el("p", {className: "wait"}, "Réflexion en cours…"));
    box.append(body);
    if (entry.note) box.append(el("p", {className: "note"}, entry.note));
    if (entry.finish === "length") box.append(el("p", {className: "note"}, "Réponse tronquée : la limite de 1 500 tokens est atteinte. Posez une question plus précise."));
    if (entry.stopped) box.append(el("p", {className: "note"}, "Réponse interrompue."));
    if (entry.error) box.append(el("p", {className: "error", role: "alert"}, entry.error.message));
    if (entry.sources.length) {
      box.append(el("p", {className: "label"}, "Sources web"),
        el("ul", {className: "sources"}, entry.sources.map(source => el("li", {}, external(source.url, source.title)))));
    }
    if (offCourse && !entry.pending && !entry.verify) {
      box.append(el("button", {type: "button", className: "secondary verify", disabled: busy || null, onclick: () => ask(entry.question, {verify: true})}, "Vérifier sur le web"));
    }
    if (entry.sent.length) {
      const count = entry.sent.length;
      box.append(el("details", {className: "sent"}, el("summary", {}, count > 1 ? `${count} extraits des cours envoyés` : "1 extrait des cours envoyé"),
        el("ul", {}, entry.sent.map(item => el("li", {}, item.url ? el("a", {href: new URL(item.url, siteRoot).href, "data-cite": item.id}, `[${item.id}]`) : `[${item.id}]`, " ", item.titre)))));
    }
    const usage = [entry.model, formatUsage(entry.usage)].filter(Boolean).join(" · ");
    if (usage && !entry.pending) box.append(el("p", {className: "usage"}, usage));
    return box;
  }
  function entryView(entry) {
    return el("article", {className: "exchange"},
      el("div", {className: "question"}, entry.verify ? el("span", {className: "tag"}, "Vérification web") : null, el("p", {}, entry.question)),
      answerView(entry));
  }
  function update(entry) {
    const view = views.get(entry);
    if (!view) return;
    const near = log.scrollHeight - log.scrollTop - log.clientHeight < 80;
    view.replaceChild(answerView(entry), view.lastChild);
    if (near) log.scrollTop = log.scrollHeight;
  }

  function render() {
    login.hidden = Boolean(key);
    bar.hidden = composer.hidden = !key;
    log.hidden = !key && !conversation.length; // après un 401, le message reste lisible au-dessus de la reconnexion
    chip.hidden = !key || !selection;
    if (selection) chipText.textContent = clip(selection.text.replace(/\s+/g, " "), 160);
    views.clear();
    const items = conversation.map(entry => { const view = entryView(entry); views.set(entry, view); return view; });
    log.replaceChildren(...(items.length ? items : [el("p", {className: "hint"}, "Posez une question sur un cours. Astuce : sélectionnez un passage avant d’ouvrir le chat pour l’envoyer en priorité.")]));
    log.setAttribute("aria-busy", String(busy));
    sendButton.disabled = busy;
    stopButton.hidden = !busy;
  }
  const save = () => session.set("conversation", JSON.stringify(conversation.slice(-12)));

  // ——— Question → réponse en streaming ———
  async function ask(text, {verify = false} = {}) {
    text = text.trim();
    if (!text || busy) return;
    if (!key) { render(); return; }
    busy = true;
    status.textContent = "";
    await loadModels();
    const chosen = models.find(item => item.id === model) || {id: model, label: model};
    const entry = {question: text, verify, answer: "", sent: [], sources: [], usage: null, finish: null, error: null, model: chosen.label, pending: true};
    conversation.push(entry);
    render();
    log.scrollTop = log.scrollHeight;
    let rows = [];
    try { rows = await loadRows(); } catch { entry.note = "Extraits des cours indisponibles : cette réponse ne s’appuie pas sur le wiki."; }
    const extracts = buildExtracts({rows, question: text, selection: resolveSelection(rows), page});
    entry.sent = extracts.map(({id, titre, cours, url}) => ({id, titre, cours, url}));
    const body = buildRequest({model: chosen.id, question: text, extracts, history: conversation.slice(0, -1), verify});
    let state = emptyAnswer(), frame = 0;
    const paint = () => { frame = 0; Object.assign(entry, {answer: state.text, sources: state.sources}); update(entry); };
    controller = new AbortController();
    try {
      const response = await fetch(`${API}/chat/completions`, {method: "POST", signal: controller.signal,
        headers: {"Authorization": `Bearer ${key}`, "Content-Type": "application/json"}, body: JSON.stringify(body)});
      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw Object.assign(new Error("HTTP"), {status: response.status, payload});
      }
      const parser = createStreamParser(event => {
        if (event.done) return;
        state = reduceChunk(state, event);
        frame ||= requestAnimationFrame(paint);
      });
      const reader = response.body.getReader(), decoder = new TextDecoder();
      for (;;) {
        const {done, value} = await reader.read();
        if (done) break;
        parser.push(decoder.decode(value, {stream: true}));
      }
      parser.push(decoder.decode());
      parser.end();
      if (state.error) {
        const code = Number(state.error.code);
        entry.error = errorFor(Number.isInteger(code) && code > 0 ? code : 500, {error: state.error});
      } else if (!state.text.trim()) entry.error = {message: "Le modèle n’a renvoyé aucun texte. Réessayez ou choisissez un autre modèle.", reconnect: false};
    } catch (error) {
      if (error && error.name === "AbortError") entry.stopped = true;
      else entry.error = errorFor(error && error.status ? error.status : 0, error && error.payload);
    }
    cancelAnimationFrame(frame);
    Object.assign(entry, {answer: state.text, sources: state.sources, usage: state.usage, finish: state.finish, pending: false});
    controller = null;
    busy = false;
    if (entry.error && entry.error.reconnect) { key = null; local.remove("key"); }
    save();
    render();
    log.scrollTop = log.scrollHeight;
    if (!panel.hidden) (key ? question : loginButton).focus({preventScroll: true});
  }

  composer.addEventListener("submit", event => {
    event.preventDefault();
    if (busy || !question.value.trim()) return;
    const text = question.value;
    question.value = "";
    ask(text);
  });
  question.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey && !event.isComposing) { event.preventDefault(); composer.requestSubmit(); }
  });
  stopButton.addEventListener("click", () => controller?.abort());
  newButton.addEventListener("click", () => {
    if (busy) controller?.abort();
    conversation = [];
    save();
    render();
    question.focus();
  });
  // Suivre une citation vers un autre cours rouvre le panneau là-bas (sur grand écran), avec la conversation.
  log.addEventListener("click", event => {
    const link = event.target.closest("a[data-cite]");
    if (link && new URL(link.href).pathname !== location.pathname) session.set("reopen", "1");
  });

  render();
  if (session.get("reopen")) {
    session.remove("reopen");
    if (!narrow.matches) open({focus: false});
  }
  finishLogin();
})();
