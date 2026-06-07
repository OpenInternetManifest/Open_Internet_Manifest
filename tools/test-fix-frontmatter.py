#!/usr/bin/env python3
# tools/test-fix-frontmatter.py - Testversie voor 1 post

import sys
import re
import hashlib
import textwrap
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def extract_block(front_body, key):
    """Robuuste extractie"""
    pattern = rf'{key}\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\w+\s*:|\n---|\Z)'
    match = re.search(pattern, front_body, re.DOTALL)
    if match:
        return textwrap.dedent(match.group(1)).strip()
    return ""

def fix_single_file(filepath, update=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content)
    if not match:
        print("❌ Geen geldige frontmatter")
        return

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)
    body = match.group(4)

    raw_markdown = extract_block(front_body, "raw_markdown")
    clean_text = extract_block(front_body, "clean_text")

    full_sha = sha256(raw_markdown)
    fuzzy_sha = sha256(clean_text)

    print(f"\n=== {filepath.name} ===")
    print(f"Raw length : {len(raw_markdown)}")
    print(f"Clean length: {len(clean_text)}")

    print("\n--- RAW MARKDOWN (dedented, eerste 6000 chars) ---")
    print(raw_markdown[:6000 ] + ("..." if len(raw_markdown) > 6000 else ""))

    print("\n--- CLEAN TEXT (eerste 6000 chars) ---")
    print(clean_text[:6000] + ("..." if len(clean_text) > 6000 else ""))

    print("\nfull_sha256  :", full_sha)
    print("fuzzy_sha256 :", fuzzy_sha)
    print("-" * 90)

    if not update:
        print("Gebruik --update om echt bij te werken\n")
        return

    # Schone frontmatter bouwen
    new_front = re.sub(r'(full_sha256|fuzzy_sha256|clean_text)\s*:\s*[\s\S]*?(?=\n\w+\s*:|\n---|\Z)', '', front_body, flags=re.DOTALL)

    new_front = new_front.strip() + f"\nraw_markdown: |\n{textwrap.indent(raw_markdown, '  ')}\n"
    new_front = new_front.strip() + f"\nclean_text: |-\n{textwrap.indent(clean_text, '  ')}\n"
    new_front = new_front.strip() + f"\nfull_sha256: {full_sha}\nfuzzy_sha256: {fuzzy_sha}\n"

    new_content = front_start + new_front.strip() + "\n" + front_end + body

    backup = filepath.with_suffix('.bak_test')
    backup.write_text(content, encoding='utf-8')

    filepath.write_text(new_content, encoding='utf-8')
    print(f"✅ Frontmatter gefixt en backup gemaakt: {backup.name}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/test-fix-frontmatter.py <bestand.md> [--update]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    update = "--update" in sys.argv

    fix_single_file(filepath, update)