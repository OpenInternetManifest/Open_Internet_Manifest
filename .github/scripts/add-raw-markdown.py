#!/usr/bin/env python3
"""
add-raw-markdown.py - Veilig raw_markdown BINNEN frontmatter toevoegen
"""

import re
from pathlib import Path

def add_raw_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'raw_markdown:' in content:
        print(f"✓ Al aanwezig: {file_path.name}")
        return False

    # Zoek de frontmatter (tussen eerste en tweede ---)
    match = re.match(r'(^---\s*\n)([\s\S]*?)(\n---\s*\n)', content, re.MULTILINE)
    if not match:
        print(f"✗ Kon frontmatter niet vinden: {file_path.name}")
        return False

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)

    # Haal de body (na frontmatter)
    body = content[match.end():].strip()

    # Maak raw_markdown blok
    raw_block = "raw_markdown: |\n" + "\n".join("  " + line for line in body.split("\n")) + "\n"

    # Combineer
    new_frontmatter = front_start + front_body.rstrip() + "\n" + raw_block + front_end

    new_content = new_frontmatter + "\n" + body

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Toegevoegd (binnen FM): {file_path.name}")
    return True

def main():
    base = Path(".")
    patterns = ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]

    updated = 0
    for pattern in patterns:
        for file in sorted(base.glob(pattern)):
            if add_raw_markdown(file):
                updated += 1

    print(f"\n🎉 Klaar! {updated} bestanden bijgewerkt.")

if __name__ == "__main__":
    main()
