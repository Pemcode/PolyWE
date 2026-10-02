(() => {
  "use strict";
  const runtime = document.getElementById("wiki-runtime");
  const form = document.getElementById("wiki-search-form");
  const compact = text => text.replace(/\s+/g, " ").trim();
  const normalize = text => String(text).toLowerCase().normalize("NFD")
    .replace(/\p{M}/gu, "")
    .replace(/t\s*8\s*\/?\s*5/g, "t85")
    .replace(/[σετγν]/g, char => ({"σ":" sigma ","ε":" epsilon ","τ":" tau ","γ":" gamma ","ν":" nu "})[char]);

  if (form && runtime) {
    const query = document.getElementById("wiki-query");
    const subject = document.getElementById("wiki-subject-filter");
    const results = document.getElementById("wiki-results");
    const status = document.getElementById("wiki-search-status");
    const params = new URL(location.href).searchParams;
    query.value = params.get("q") || "";
    subject.value = params.get("matiere") || "";
    if (subject.selectedIndex < 0) subject.value = "";
    let rowsPromise;
    let revision = 0;
    let debounce;
    const getRows = () => rowsPromise ||= fetch(new URL("recherche.json", runtime.src))
      .then(response => {
        if (!response.ok) throw new Error("Index indisponible");
        return response.json();
      }).catch(error => { rowsPromise = null; throw error; });

    async function search() {
      const call = ++revision;
      const terms = normalize(query.value).trim().split(/\s+/).filter(Boolean);
      const selected = subject.value;
      const url = new URL(location.href);
      query.value.trim() ? url.searchParams.set("q", query.value.trim()) : url.searchParams.delete("q");
      selected ? url.searchParams.set("matiere", selected) : url.searchParams.delete("matiere");
      history.replaceState(null, "", url);
      results.replaceChildren();
      if (!terms.length && !selected) {
        status.textContent = "Explorez les matières ci-dessous ou recherchez un sujet précis.";
        return;
      }
      status.textContent = "Recherche…";
      try {
        const rows = await getRows();
        if (call !== revision) return;
        const matches = rows.filter(row => !selected || row.matiere === selected)
          .map(row => {
            const title = normalize(row.titre);
            const course = normalize(row.cours);
            const all = normalize([row.titre, row.cours, row.matiere_titre, ...row.mots_cles, ...row.ressources].join(" "));
            if (!terms.every(term => all.includes(term))) return null;
            const score = terms.reduce((sum, term) => sum + (title.includes(term) ? 10 : course.includes(term) ? 3 : 1), 0);
            return {row, score};
          }).filter(Boolean).sort((a, b) => b.score - a.score || a.row.titre.localeCompare(b.row.titre, "fr"));
        status.textContent = matches.length ? `${matches.length} résultat${matches.length > 1 ? "s" : ""}.` : "Aucun résultat. Essayez un autre mot ou une autre matière.";
        const fragment = document.createDocumentFragment();
        for (const {row} of matches) {
          const li = document.createElement("li");
          const anchor = document.createElement("a");
          anchor.href = row.url;
          anchor.textContent = row.titre;
          const context = document.createElement("small");
          context.textContent = `${row.matiere_titre} · ${row.type === "section" ? row.cours : row.type === "application" ? "Application interactive" : "Cours complet"}`;
          li.append(anchor, context);
          fragment.append(li);
        }
        results.append(fragment);
      } catch {
        if (call === revision) status.textContent = "La recherche est indisponible. Vous pouvez parcourir les matières ci-dessous.";
      }
    }
    form.addEventListener("submit", event => { event.preventDefault(); clearTimeout(debounce); search(); });
    query.addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(search, 150); });
    subject.addEventListener("change", search);
    if (query.value || subject.value) search();
  }

  const navigation = document.querySelector(".wiki-nav");
  if (!navigation) return;
  const status = document.getElementById("wiki-share-status");
  const title = document.querySelector('meta[name="wiki-course-title"]')?.content || document.title;
  const targetFor = hash => {
    try { return document.getElementById(decodeURIComponent(hash.replace(/^#/, ""))); }
    catch { return null; }
  };
  const headingFor = target => target?.matches("h2,h3") ? target : target?.querySelector("h2,h3");

  // Ces boutons sont ajoutés au document affiché, jamais aux sources pédagogiques.
  for (const anchor of navigation.querySelectorAll('.wiki-course-menu a[href^="#"]')) {
    const target = targetFor(anchor.hash);
    const heading = headingFor(target);
    if (!heading) continue;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "wiki-section-share";
    button.textContent = "Partager cette section";
    button.dataset.wikiShare = "native";
    button.dataset.wikiAnchor = anchor.hash;
    heading.insertAdjacentElement("afterend", button);
  }

  async function copyLink(url) {
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Copie non disponible");
      await navigator.clipboard.writeText(url);
      status.textContent = "Lien copié.";
    } catch {
      const fallback = navigation.querySelector(".wiki-copy-fallback");
      fallback.hidden = false;
      const input = fallback.querySelector("input");
      input.value = url;
      input.focus();
      input.select();
      status.textContent = "Sélectionnez et copiez ce lien.";
    }
  }

  document.addEventListener("click", async event => {
    const button = event.target.closest("[data-wiki-share]");
    if (!button) return;
    const url = new URL(location.href);
    if (button.dataset.wikiAnchor) url.hash = button.dataset.wikiAnchor;
    const heading = headingFor(targetFor(url.hash));
    const text = heading ? `${title} — ${compact(heading.textContent).replace(/^\d+\s*(?=[A-ZÀ-Ü])/, "")}` : title;
    status.textContent = "";
    if (button.dataset.wikiShare === "native" && navigator.share) {
      try {
        await navigator.share({title, text, url: url.href});
        status.textContent = "Partage ouvert.";
        return;
      } catch (error) {
        if (error.name === "AbortError") return;
      }
    }
    await copyLink(url.href);
  });

  function revealTarget() {
    const target = targetFor(location.hash);
    if (!target) return;
    for (let parent = target; parent; parent = parent.parentElement) {
      if (parent.tagName === "DETAILS") parent.open = true;
    }
  }
  addEventListener("hashchange", revealTarget);
  revealTarget();
})();
