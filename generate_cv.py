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

    lines.extend([f"## {title}", ""])

    if isinstance(content, str):
        lines.extend([content.strip(), ""])
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
personal = cv.get("personal", {}) or {}
name = personal.get("name", {}) or {}

if isinstance(name, dict):
    full_name = name.get("full", "") or name.get("display", "")
    if not full_name:
        full_name = " ".join(
            str(value) for value in name.values() if value
        )
else:
    full_name = str(name) if name else ""

if full_name:
    lines.extend([f"# {full_name}", ""])

if personal.get("title"):
    lines.extend([f"**{personal['title']}**", ""])

for field in ("email", "phone", "location", "website", "linkedin"):
    value = personal.get(field)
    if value:
        lines.append(f"**{field.capitalize()}:** {value}")

lines.append("")

add_section(lines, "Προφίλ", cv.get("profile"))
add_section(lines, "Εκπαίδευση", cv.get("education"))
add_section(lines, "Επαγγελματική εμπειρία", cv.get("experience"))
add_section(lines, "Πιστοποιήσεις", cv.get("certifications"))

OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"Δημιουργήθηκε το αρχείο: {OUTPUT_FILE}")
