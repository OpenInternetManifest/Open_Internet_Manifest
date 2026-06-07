#!/usr/bin/env python3
# tools/fix-hashes-placement.py - Zeer robuuste hash fix

import sys
import re
import hashlib
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Frontmatter vinden
    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content)
    if not match:
        print(f"❌ Geen frontmatter: {filepath.name}")
        return False

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)
    body = match.group(4)

    # raw_markdown ophalen (meerdere patronen)
    raw_match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n(.*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)
    clean_match = re.search(r'clean_text\s*:\s*\|-?\s*\n(.*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)

    raw_markdown = raw_match.group(1).strip() if raw_match else ""
    clean_text = clean_match.group(1).strip() if clean_match else ""

    if not raw_markdown:
        print(f"⚠️  Geen raw_markdown: {filepath.name}")
        return False

    full_sha = sha256(raw_markdown)
    fuzzy_sha = sha256(clean_text)

    # Alle oude hashes verwijderen
    new_front = re.sub(r'(full_sha256|fuzzy_sha256)\s*:\s*[^\n]+\n?', '', front_body)

    # Nieuwe hashes toevoegen
    new_front = new_front.strip() + f"\nfull_sha256: {full_sha}\nfuzzy_sha256: {fuzzy_sha}\n"

    new_content = front_start + new_front.strip() + "\n" + front_end + body

    # Backup + schrijven
    backup = filepath.with_suffix('.bak_final')
    backup.write_text(content, encoding='utf-8')

    filepath.write_text(new_content, encoding='utf-8')
    print(f"✅ Fixed: {filepath.name} | full: {full_sha[:8]}... | fuzzy: {fuzzy_sha[:8]}...")

    return True


if __name__ == "__main__":
    base_dir = Path("_social-posts")
    total = 0

    for lang in ["nl", "en"]:
        dir_path = base_dir / lang
        if not dir_path.exists():
            continue
        print(f"\n=== Fixing {lang} ===")
        count = 0
        for file in sorted(dir_path.glob("day-*.md")):
            if fix_file(file):
                count += 1
        print(f"   → {count} bestanden gefixt")
        total += count

    print(f"\nKlaar! {total} bestanden verwerkt.")