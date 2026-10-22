from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
CV_FILE = ROOT / "cv.yml"
OUTPUT_FILE = ROOT / "cv-generated.md"

with CV_FILE.open("r", encoding="utf-8") as file:
    cv = yaml.safe_load(file) or {}


def add_items(lines, items, fields):
    if not isinstance(items, list):
        return

    for item in items:
        if not isinstance(item, dict):
            continue

        for field, label in fields:
            value = item.get(field)
            if value:
                lines.append(f"**{label}:** {value}")

        lines.append("")


lines = []
personal = cv.get("personal") or {}
name = personal.get("name") or {}

if isinstance(name, dict):
    full_name = " ".join(str(v) for v in name.values() if v)
else:
    full_name = str(name)

if full_name:
    lines.extend([f"# {full_name}", ""])

if personal.get("title"):
    lines.extend([f"**{personal['title']}**", ""])

for field in ("email", "phone", "location", "website", "linkedin"):
    value = personal.get(field)
    if value:
        lines.append(f"**{field.capitalize()}:** {value}")

lines.append("")


def add_section(lines, title, content):
    if not content:
        return
    lines.extend([f"## {title}", ""])
    if isinstance(content, str):
        lines.extend([content.strip(), ""])
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                for key, value in item.items():
                    if value:
                        lines.append(f"**{key}:** {value}")
                lines.append("")
            else:
                lines.extend([f"- {item}", ""])
    elif isinstance(content, dict):
        for key, value in content.items():
            if value:
                lines.extend([f"**{key}:** {value}", ""])


add_section(lines, "Προφίλ", cv.get("profile"))

education = cv.get("education") or []
if education:
    lines.extend(["## Εκπαίδευση", ""])
    for item in education:
        if item.get("degree"):
            lines.append(f"**{item['degree']}**")
        if item.get("institution"):
            lines.append(item["institution"])
        lines.append("")

experience = cv.get("experience") or []
if experience:
    lines.extend(["## Επαγγελματική εμπειρία", ""])
    for item in experience:
        if item.get("position"):
            lines.append(f"**{item['position']}**")
        if item.get("organization"):
            lines.append(item["organization"])
        if item.get("period"):
            lines.append(f"*{item['period']}*")
        lines.append("")

certifications = cv.get("certifications") or []
if certifications:
    lines.extend(["## Πιστοποιήσεις", ""])
    for item in certifications:
        if item.get("name"):
            lines.append(f"**{item['name']}**")
        if item.get("institution"):
            lines.append(item["institution"])
        lines.append("")

OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"Δημιουργήθηκε το αρχείο: {OUTPUT_FILE}")
