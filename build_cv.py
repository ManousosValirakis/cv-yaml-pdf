from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent

# Διαβάζουμε τα δεδομένα του βιογραφικού
with open(ROOT / "cv.yml", encoding="utf-8") as file:
    cv = yaml.safe_load(file)

# Φάκελος προτύπων HTML
env = Environment(
    loader=FileSystemLoader(ROOT / "templates")
)

template = env.get_template("cv.html")
html = template.render(cv=cv)

# Δημιουργία HTML
(ROOT / "index.html").write_text(html, encoding="utf-8")

# Δημιουργία PDF
HTML(string=html, base_url=str(ROOT)).write_pdf(
    str(ROOT / "cv.pdf")
)

print("Το βιογραφικό δημιουργήθηκε σε HTML και PDF.")
