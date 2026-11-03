
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent

with (ROOT / "cv.yml").open(encoding="utf-8") as f:
    cv = yaml.safe_load(f) or {}

personal = cv.get("personal") or {}
name = personal.get("name") or ""

if isinstance(name, dict):
    name = " ".join(str(v) for v in name.values() if v)

lines = []

if name:
    lines.extend([f"# {name}", ""])

if personal.get("title"):
    lines.extend([f"**{personal['title']}**", ""])

if personal.get("location"):
    lines.extend([str(personal["location"]), ""])

if personal.get("website"):
    url = personal["website"]
    lines.extend([f"[Προσωπική ιστοσελίδα]({url})", ""])

for field, label in (
    ("email", "Email"),
    ("phone", "Τηλέφωνο"),
    ("linkedin", "LinkedIn"),
):
    if personal.get(field):
        lines.extend([f"**{label}:** {personal[field]}", ""])

profile = cv.get("profile")
if profile:
    lines.extend(["## Προφίλ", "", str(profile).strip(), ""])

education = cv.get("education") or []
if education:
    lines.extend(["## Εκπαίδευση", ""])
    for item in education:
        lines.append(
            f"- **{item.get('degree', '')}** — "
            f"{item.get('institution', '')}"
        )
    lines.append("")

experience = cv.get("experience") or []
if experience:
    lines.extend(["## Επαγγελματική εμπειρία", ""])
    for item in experience:
        lines.append(
            f"- **{item.get('position', '')}** — "
            f"{item.get('organization', '')} "
            f"({item.get('period', '')})"
        )
    lines.append("")

certifications = cv.get("certifications") or []
if certifications:
    lines.extend(["## Πιστοποιήσεις", ""])
    for item in certifications:
        lines.append(
            f"- **{item.get('name', '')}** — "
            f"{item.get('institution', '')}"
        )
    lines.append("")

content = "\n".join(lines)

# Markdown used by Pandoc for PDF generation
(ROOT / "cv-generated.md").write_text(
    content, encoding="utf-8"
)

# Jekyll page with the existing PDF download button
header = """---
layout: default
title: Βιογραφικό
---

"""

button = """
<a href="cv.pdf" download="Manousos-Valirakis-CV.pdf"
   style="display:inline-block;
          background-color:#2457a7;
          color:white;
          padding:12px 22px;
          border-radius:8px;
          text-decoration:none;
          font-weight:bold;">
  📄 Κατέβασε το βιογραφικό σε PDF
</a>

"""

# Place the download button before the profile section
if "## Προφίλ" in content:
    content_web = content.replace(
        "## Προφίλ", button + "## Προφίλ", 1
    )
else:
    content_web = content + "\n" + button

(ROOT / "index.md").write_text(
    header + content_web, encoding="utf-8"
)

print("Created cv-generated.md and index.md from cv.yml")

