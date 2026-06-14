#!/usr/bin/env python3
# tools/fix-yaml-frontmatter.py - Repareert YAML problemen na clean_text aanpassingen

import sys
import re
from pathlib import Path

def fix_frontmatter(filepath):
    filepath = Path(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Zorg dat frontmatter goed begint en eindigt
    if not content.strip().startswith('---'):
        content = '---\n' + content

    # Repareer clean_text (maak quoted single-line)
    def clean_clean_text(match):
        text = match.group(1).strip()
        text = re.sub(r'\s+', ' ', text)
        return f'clean_text: "{text}"'

    content = re.sub(
        r'clean_text\s*:\s*(?:\|-?\s*\n)?([\s\S]*?)(?=\n\w+\s*:|\n---|\Z)',
        clean_clean_text,
        content,
        flags=re.DOTALL
    )

    # Zorg voor dubbele newlines rond frontmatter
    content = re.sub(r'---\s*---', '---\n---', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Gefixt: {filepath.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/fix-yaml-frontmatter.py <bestand.md> of bulk")
        sys.exit(1)

    for arg in sys.argv[1:]:
        if Path(arg).is_file():
            fix_frontmatter(arg)