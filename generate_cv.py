from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
CV_FILE = ROOT / "cv.yml"
OUTPUT_FILE = ROOT / "cv-generated.md"

with CV_FILE.open("r", encoding="utf-8") as file:
    cv = yaml.safe_load(file) or {}


def add_section(lines, title, content):
    if not content:
        return

    lines.append(f"## {title}")
    lines.append("")

    if isinstance(content, str):
        lines.append(content.strip())
    elif isinstance(content, dict):
        for key, value in content.items():
            if value:
                lines.append(f"**{key}:** {value}")
                lines.append("")
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                for key, value in item.items():
                    if value:
                        lines.append(f"**{key}:** {value}")
                lines.append("")
            else:
                lines.append(f"- {item}")

    lines.append("")


lines = []

personal = cv.get("personal", {})
if isinstance(personal, dict):
    name = personal.get("name", "")
    if name:
        lines.extend([f"# {name}", ""])
    for key, value in personal.items():
        if key != "name" and value:
            lines.append(f"**{key}:** {value}")
    lines.append("")

add_section(lines, "Προφίλ", cv.get("profile"))
add_section(lines, "Εκπαίδευση", cv.get("education"))
add_section(lines, "Επαγγελματική εμπειρία", cv.get("experience"))
add_section(lines, "Πιστοποιήσεις", cv.get("certifications"))

OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

print(f"Δημιουργήθηκε το αρχείο: {OUTPUT_FILE}")
