#!/usr/bin/env python3
# tools/update-all-hashes.py - Bulk update full + fuzzy hashes

import sys
import re
import hashlib
import textwrap
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def strong_dedent(text):
    if not text:
        return ""
    return textwrap.dedent(text).strip()

def update_file(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content)
    if not match:
        return False

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)
    body = match.group(4)

    # raw_markdown
    raw_match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)
    clean_match = re.search(r'clean_text\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)

    raw_markdown = strong_dedent(raw_match.group(1)) if raw_match else ""
    clean_text = clean_match.group(1).strip() if clean_match else ""

    full_sha = sha256(raw_markdown)
    fuzzy_sha = sha256(clean_text)

    # Update frontmatter
    new_front = re.sub(r'(full_sha256|fuzzy_sha256)\s*:\s*[^\n]+\n?', '', front_body)
    new_front = new_front.strip() + f"\nfull_sha256: {full_sha}\nfuzzy_sha256: {fuzzy_sha}\n"

    new_content = front_start + new_front.strip() + "\n" + front_end + body

    if dry_run:
        print(f"DRY-RUN: Would update {filepath.name}")
    else:
        backup = filepath.with_suffix('.bak_final')
        backup.write_text(content, encoding='utf-8')
        
        filepath.write_text(new_content, encoding='utf-8')
        print(f"✅ Updated: {filepath.name}")

    return True


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-d" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE ===\n")

    base_dir = Path("_social-posts")
    total = 0

    for lang in ["nl", "en"]:
        dir_path = base_dir / lang
        if not dir_path.exists():
            continue
        print(f"\n=== {lang.upper()} ===")
        count = 0
        for file in sorted(dir_path.glob("day-*.md")):
            if update_file(file, dry_run):
                count += 1
        print(f"   → {count} bestanden verwerkt")
        total += count

    print(f"\nKlaar! Totaal {total} bestanden verwerkt ({'DRY RUN' if dry_run else 'echt bijgewerkt'})")