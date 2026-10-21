from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"
HTML_FILE = SITE / "index.html"
PDF_FILE = SITE / "cv.pdf"

if not HTML_FILE.exists():
    raise FileNotFoundError("Δεν βρέθηκε η ιστοσελίδα Jekyll.")

with TemporaryDirectory() as temp_dir:
    temp_pdf = Path(temp_dir) / "cv.pdf"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto(HTML_FILE.as_uri(), wait_until="networkidle")

        page.add_style_tag(content="""
            .webring,
            a[download] {
                display: none !important;
            }

            body {
                background: white !important;
            }
        """)

        page.pdf(
            path=str(temp_pdf),
            format="A4",
            print_background=True,
            prefer_css_page_size=True
        )

        browser.close()

    SITE.mkdir(parents=True, exist_ok=True)
    copy2(temp_pdf, PDF_FILE)

print("Το PDF δημιουργήθηκε:", PDF_FILE)
