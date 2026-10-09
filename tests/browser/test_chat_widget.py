"""Assistant de révision : connexion PKCE, réponse en streaming, citations, erreurs et mise en page (S25).

OpenRouter est simulé : ces parcours ne demandent ni compte, ni réseau. Ils tournent à la racine et sous /promo/."""
import base64
import hashlib
import json
from urllib.parse import parse_qs, urlsplit

import pytest
from playwright.sync_api import expect

from test_journeys import site

CORS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Authorization, Content-Type",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS"}
MODELS = {"data": [
    {"id": "openai/gpt-6.1-sol", "name": "OpenAI: GPT-6.1 Sol", "supported_parameters": ["tools", "reasoning"]},
    {"id": "mistralai/mistral-large-4-0", "name": "Mistral: Large 4", "supported_parameters": ["tools"]},
    {"id": "anthropic/claude-opus-5.5", "name": "Anthropic: Claude Opus 5.5", "supported_parameters": ["reasoning"]}]}
DESKTOP = {"width": 1366, "height": 768}
USAGE = {"prompt_tokens": 900, "completion_tokens": 80, "total_tokens": 980, "cost": 0.0031}


def answer(text, *, sources=()):
    delta = {"content": text}
    if sources:
        delta["annotations"] = [{"type": "url_citation", "url_citation": {"url": url, "title": title}} for url, title in sources]
    chunks = [{"choices": [{"delta": delta}]}, {"choices": [{"delta": {}, "finish_reason": "stop"}], "usage": USAGE}]
    return ": OPENROUTER PROCESSING\n\n" + "".join(f"data: {json.dumps(chunk)}\n\n" for chunk in chunks) + "data: [DONE]\n\n"


class OpenRouter:
    """Faux OpenRouter : page d’autorisation, modèles, échange du code et complétions."""

    def __init__(self, page):
        self.requests, self.exchanges, self.replies = [], [], []
        self.challenge = None
        page.route("https://openrouter.ai/**", self.handle)

    def handle(self, route):
        request = route.request
        if request.method == "OPTIONS":
            return route.fulfill(status=204, headers=CORS)
        url = urlsplit(request.url)
        if url.path == "/auth":
            params = parse_qs(url.query)
            self.challenge = params["code_challenge"][0]
            back = params["callback_url"][0]
            target = back + ("&" if "?" in back else "?") + "code=code-de-test"
            return route.fulfill(status=200, content_type="text/html", body=f"<script>location.replace({json.dumps(target)})</script>")
        if url.path == "/api/v1/models":
            return route.fulfill(status=200, json=MODELS, headers=CORS)
        if url.path == "/api/v1/auth/keys":
            self.exchanges.append(request.post_data_json)
            return route.fulfill(status=200, json={"key": "sk-or-v1-test", "user_id": "u"}, headers=CORS)
        if url.path == "/api/v1/chat/completions":
            self.requests.append({"body": request.post_data_json, "authorization": request.headers.get("authorization")})
            reply = self.replies.pop(0) if self.replies else answer("Réponse.")
            if reply == "abort":
                return route.abort("failed")
            if isinstance(reply, tuple):
                return route.fulfill(status=reply[0], json=reply[1], headers=CORS)
            return route.fulfill(status=200, body=reply, headers={**CORS, "Content-Type": "text/event-stream"})
        return route.abort()


@pytest.fixture
def chat(site):
    page, base = site
    return page, base, OpenRouter(page)


@pytest.fixture
def connected(chat):
    page, base, api = chat
    page.add_init_script("localStorage.setItem('polywe_chat_key', 'sk-or-v1-test')")
    return page, base, api


def panel(page):
    return page.get_by_role("dialog", name="Assistant de révision")


def open_chat(page):
    page.get_by_role("button", name="Chat", exact=True).click()
    expect(panel(page)).to_be_visible()


def ask(page, text):
    box = page.get_by_label("Votre question")
    box.fill(text)
    box.press("Enter")


def test_login_with_pkce_returns_to_the_same_section_and_keeps_only_prefixed_keys(chat):
    page, base, api = chat
    page.goto(base + "Thermique/introduction.html#calcul")
    before = set(page.evaluate("Object.keys(localStorage)"))
    open_chat(page)
    expect(panel(page).get_by_text("votre propre compte OpenRouter")).to_be_visible()
    expect(panel(page).get_by_text("facturés sur votre compte OpenRouter")).to_be_visible()
    panel(page).get_by_role("button", name="Se connecter avec OpenRouter").click()
    expect(panel(page).get_by_role("status")).to_have_text("Connecté à OpenRouter. Posez votre question.")
    assert page.url == base + "Thermique/introduction.html#calcul", "le code disparaît de l’adresse, l’ancre revient"
    exchange, = api.exchanges
    assert exchange["code"] == "code-de-test" and exchange["code_challenge_method"] == "S256"
    digest = hashlib.sha256(exchange["code_verifier"].encode()).digest()
    assert base64.urlsafe_b64encode(digest).rstrip(b"=").decode() == api.challenge
    assert page.evaluate("localStorage.getItem('polywe_chat_key')") == "sk-or-v1-test"
    added = set(page.evaluate("Object.keys(localStorage)")) - before
    assert added and all(name.startswith("polywe_chat_") for name in added), added
    expect(page.get_by_label("Votre question")).to_be_focused()
    panel(page).get_by_role("button", name="Se déconnecter").click()
    assert page.evaluate("localStorage.getItem('polywe_chat_key')") is None
    expect(panel(page).get_by_role("button", name="Se connecter avec OpenRouter")).to_be_visible()


def test_a_forged_code_in_a_shared_link_is_never_exchanged(chat):
    page, base, api = chat
    page.goto(base + "?code=vole")
    expect(page.get_by_role("button", name="Chat", exact=True)).to_be_visible()
    page.wait_for_timeout(300)
    assert api.exchanges == []
    assert page.url.endswith("?code=vole")
    assert page.evaluate("localStorage.getItem('polywe_chat_key')") is None


def test_answer_links_cited_sections_flags_unknown_ids_and_never_renders_model_html(connected):
    page, base, api = connected
    api.replies.append(answer(
        "Le préchauffage se règle avec soin [TH-01-INTRO]. Valeur trouvée ailleurs [RDM-99-C9].\n"
        "<img src=x onerror=\"window.pwned=1\"> **Retenir** :\n- ralentir le refroidissement\n- [piège](javascript:window.pwned=2)",
        sources=[("https://www.twi-global.com/technical-knowledge/faqs/preheat", "TWI — préchauffage")]))
    page.set_viewport_size(DESKTOP)
    page.goto(base + "Thermique/introduction.html")
    open_chat(page)
    model = panel(page).get_by_label("Modèle")
    expect(model).to_have_value("openai/gpt-6.1-sol")
    assert model.locator("option").all_inner_texts() == ["GPT-6.1 Sol", "Mistral Large 4"], "Claude sans outils est écarté"
    ask(page, "Pourquoi faut-il un préchauffage ?")
    log = panel(page).get_by_role("log")
    expect(log.get_by_role("link", name="TH-01-INTRO", exact=True)).to_have_attribute("href", base + "Thermique/introduction.html#intro")
    expect(log.get_by_text("source non vérifiée", exact=True)).to_have_count(1)
    expect(log.get_by_text('<img src=x onerror="window.pwned=1">')).to_be_visible()
    expect(log.locator("img")).to_have_count(0)
    expect(log.get_by_role("link", name="piège")).to_have_count(0)
    expect(log.locator("strong", has_text="Retenir")).to_be_visible()
    expect(log.locator(".md li")).to_have_count(2)
    expect(log.get_by_role("link", name="TWI — préchauffage")).to_have_attribute("rel", "noopener noreferrer nofollow")
    expect(log.get_by_text("980 tokens", exact=False)).to_be_visible()
    assert page.evaluate("window.pwned") is None
    request, = api.requests
    assert request["authorization"] == "Bearer sk-or-v1-test"
    body = request["body"]
    assert body["model"] == "openai/gpt-6.1-sol" and body["stream"] is True and body["max_tokens"] == 1500
    assert body["tools"][0]["type"] == "openrouter:web_search"
    assert "[TH-01-INTRO] Préchauffage — Comprendre le préchauffage\nComprendre le préchauffage\nUne explication." in body["messages"][-1]["content"]
    page.reload()
    open_chat(page)
    expect(panel(page).get_by_text("Pourquoi faut-il un préchauffage ?")).to_be_visible()


def test_off_course_answer_gets_a_badge_and_can_be_checked_on_the_web(connected):
    page, base, api = connected
    api.replies += [answer("Hors cours : le module de Young d’un acier vaut environ 210 GPa."),
                    answer("Environ 210 GPa pour un acier de construction.", sources=[("https://www.twi-global.com/a", "TWI")])]
    page.goto(base + "Thermique/introduction.html")
    open_chat(page)
    ask(page, "Quel est le module de Young de l’acier ?")
    log = panel(page).get_by_role("log")
    expect(log.get_by_text("Hors cours", exact=True)).to_be_visible()
    log.get_by_role("button", name="Vérifier sur le web").click()
    expect(log.get_by_role("link", name="TWI", exact=True)).to_be_visible()
    messages = api.requests[1]["body"]["messages"]
    assert [message["role"] for message in messages] == ["system", "user", "assistant", "user"]
    assert messages[2]["content"].startswith("Hors cours")
    assert "CONSIGNE\nFais UNE recherche web" in messages[-1]["content"]
    expect(log.get_by_text("Vérification web", exact=True)).to_be_visible()


@pytest.mark.parametrize("reply, message", [
    ((401, {"error": {"code": 401, "message": "No auth credentials found"}}), "Reconnectez-vous"),
    ((402, {"error": {"code": 402, "message": "Insufficient credits"}}), "Crédits OpenRouter insuffisants"),
    ((429, {"error": {"code": 429, "message": "Rate limited"}}), "Trop de requêtes"),
    ("abort", "Connexion à OpenRouter impossible"),
], ids=["401", "402", "429", "reseau"])
def test_errors_are_explained_in_french(connected, reply, message):
    page, base, api = connected
    api.replies.append(reply)
    page.goto(base + "Thermique/introduction.html")
    open_chat(page)
    ask(page, "Préchauffage ?")
    expect(panel(page).get_by_role("alert")).to_contain_text(message)
    if reply[0] == 401:
        assert page.evaluate("localStorage.getItem('polywe_chat_key')") is None
        expect(panel(page).get_by_role("button", name="Se connecter avec OpenRouter")).to_be_visible()
    else:
        expect(page.get_by_label("Votre question")).to_be_visible()


def test_selected_text_is_sent_first_with_the_id_of_its_section(connected):
    page, base, api = connected
    page.set_viewport_size(DESKTOP)
    page.goto(base + "Thermique/introduction.html")
    page.evaluate("""() => { const range = document.createRange(); range.selectNodeContents(document.querySelector('#intro p'));
                     getSelection().removeAllRanges(); getSelection().addRange(range); }""")
    open_chat(page)
    expect(panel(page).get_by_text("Une explication.", exact=True)).to_be_visible()
    ask(page, "Tu peux détailler ?")
    expect(panel(page).get_by_role("log").get_by_text("Réponse.", exact=True)).to_be_visible()
    content = api.requests[0]["body"]["messages"][-1]["content"]
    assert content.startswith("EXTRAITS\n[TH-01-INTRO] Préchauffage — Texte sélectionné · Comprendre le préchauffage\nUne explication.\n\n"), content
    panel(page).get_by_role("button", name="Retirer le texte sélectionné").click()
    expect(panel(page).get_by_text("Texte sélectionné, envoyé en priorité")).to_be_hidden()


def test_phone_launcher_stays_above_the_menu_and_escape_closes_the_panel(chat):
    page, base, _ = chat
    page.goto(base + "Thermique/introduction.html")
    launcher = page.get_by_role("button", name="Chat", exact=True)
    menu = page.get_by_role("button", name="Menu", exact=True)
    expect(launcher).to_be_visible()
    chat_box, menu_box = launcher.bounding_box(), menu.bounding_box()
    assert chat_box["y"] + chat_box["height"] <= menu_box["y"], "le bouton Chat reste au-dessus du bouton Menu"
    assert chat_box["x"] + chat_box["width"] <= 390
    launcher.click()
    dialog = panel(page)
    box = dialog.bounding_box()
    assert (box["x"], box["y"], box["width"], box["height"]) == (0, 0, 390, 844), "plein écran sur téléphone"
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    expect(dialog.get_by_role("button", name="Se connecter avec OpenRouter")).to_be_focused()
    page.keyboard.press("Escape")
    expect(dialog).to_be_hidden()
    expect(launcher).to_be_focused()
    expect(launcher).to_have_attribute("aria-expanded", "false")


def test_panel_follows_the_system_theme_and_the_page_theme_choice(chat):
    page, base, _ = chat
    page.set_viewport_size(DESKTOP)
    page.emulate_media(color_scheme="dark")
    page.goto(base + "Thermique/introduction.html")
    open_chat(page)
    background = lambda: panel(page).evaluate("node => getComputedStyle(node).backgroundColor")
    assert background() == "rgb(12, 18, 23)"
    page.evaluate("document.documentElement.dataset.theme = 'light'")
    assert background() == "rgb(251, 251, 248)"
    box = panel(page).bounding_box()
    assert box["x"] + box["width"] <= DESKTOP["width"] - 8 and box["y"] >= 8
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
