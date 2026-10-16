"""Observer et agrandir les photos du cours, hors ligne et dans le wiki (S33)."""
from functools import partial
from http.server import ThreadingHTTPServer
import threading

import pytest
from playwright.sync_api import expect, sync_playwright

from conftest import copy_real_project
from test_journeys import QuietHandler
from wiki.build import build


@pytest.fixture(scope="module")
def photo_course(tmp_path_factory):
    root = tmp_path_factory.mktemp("photos")
    data, _ = copy_real_project(root, planning=True)
    course = next(c for c in data["cours"] if c["id"] == "essais-03")
    output = build(root)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(root)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield root, course, f"http://127.0.0.1:{server.server_port}/{output.name}/"
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


@pytest.mark.parametrize("mode", ["autonome", "wiki"])
def test_observe_photos_offline_and_return_to_reading(photo_course, mode):
    root, course, base = photo_course
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--host-resolver-rules=MAP static.cloudflareinsights.com ~NOTFOUND"])
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        if mode == "autonome":
            context.set_offline(True)
            url = (root / course["fichier"]).as_uri()
        else:
            url = base + course["url"]
        page.goto(url, wait_until="domcontentloaded")
        context.set_offline(True)
        if mode == "wiki":
            expect(page.locator('#wiki-panel a[href$="#photo-viewer-title"]')).to_have_count(0)
        photos = page.locator("figure.course-photo")
        expect(photos).to_have_count(4)
        for photo in photos.all():
            photo.scroll_into_view_if_needed()
            picture = photo.locator("img")
            expect(picture).to_be_visible()
            expect(picture).to_have_js_property("complete", True)
            assert picture.evaluate("img => img.naturalWidth >= 900")
            assert picture.get_attribute("alt")
            expect(photo.locator(".photo-credit a").first).to_be_visible()
            opener = photo.get_by_role("button", name="Agrandir", exact=False)
            opener.focus()
            page.keyboard.press("Enter")
            viewer = page.get_by_role("dialog", name="Photographie agrandie")
            expect(viewer).to_be_visible()
            expect(viewer.locator("img")).to_have_attribute("alt", picture.get_attribute("alt"))
            expect(viewer.locator(".photo-credit")).to_be_visible()
            zoom = viewer.locator("#photo-zoom")
            zoom.click()
            expect(zoom).to_have_attribute("aria-pressed", "true")
            assert viewer.locator(".photo-viewer-stage").evaluate("el => el.scrollWidth > el.clientWidth")
            zoom.click()
            expect(zoom).to_have_attribute("aria-pressed", "false")
            page.keyboard.press("Escape")
            expect(viewer).not_to_be_visible()
            expect(opener).to_be_focused()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        expect(page.locator("#photos-attaque")).to_contain_text("champs différents")
        page.locator("#photos-attaque").get_by_text("Voir les repères", exact=True).click()
        expect(page.locator("#photos-attaque details")).to_have_attribute("open", "")
        page.locator('#m6d button[data-k="pore"]').click()
        expect(page.locator("#m6msg")).to_contain_text("soufflure", ignore_case=True)
        assert not errors
        browser.close()
