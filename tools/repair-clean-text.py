#!/usr/bin/env python3
# tools/repair-clean-text.py - Herstelt kapotte clean_text frontmatter

import sys
import re
from pathlib import Path

def repair_file(filepath):
    filepath = Path(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Haal bestaande clean_text eruit (multi-line of kapot)
    match = re.search(r'clean_text\s*:\s*(?:["\']|\|-?\s*\n)?([\s\S]*?)(?=\n\w+\s*:|\n---|\Z)', content, re.DOTALL)
    if not match:
        print(f"⚠️  Geen clean_text: {filepath.name}")
        return

    raw_text = match.group(1).strip()
    clean_text = re.sub(r'\s+', ' ', raw_text).strip()

    # Vervang hele clean_text blok door nette quoted versie
    new_clean = f'clean_text: "{clean_text}"'

    new_content = re.sub(
        r'clean_text\s*:\s*(?:["\']|\|-?\s*\n)?[\s\S]*?(?=\n\w+\s*:|\n---|\Z)',
        new_clean,
        content,
        flags=re.DOTALL
    )

    # Extra veiligheid: zorg dat frontmatter goed eindigt
    if '---' not in new_content[-100:]:
        new_content = new_content.strip() + "\n---\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Hersteld: {filepath.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/repair-clean-text.py <bestand.md> of bulk")
        sys.exit(1)

    for arg in sys.argv[1:]:
        if Path(arg).is_file() and arg.endswith('.md'):
            repair_file(arg)