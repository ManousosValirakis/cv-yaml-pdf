from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"
HTML_FILE = SITE / "index.html"
TEMP_PDF = ROOT / "cv-generated.pdf"

if not HTML_FILE.exists():
    raise FileNotFoundError("Δεν βρέθηκε η ιστοσελίδα Jekyll.")

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
        path=str(TEMP_PDF),
        format="A4",
        print_background=True,
        prefer_css_page_size=True
    )

    browser.close()

print("Το PDF δημιουργήθηκε:", TEMP_PDF)
