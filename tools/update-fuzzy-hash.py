#!/usr/bin/env python3
# tools/update-fuzzy-hash.py

import sys
import re
import hashlib
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def update_fuzzy(filepath, update=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content)
    if not match:
        return False

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)
    body = match.group(4)

    clean_match = re.search(r'clean_text\s*:\s*\|-?\s*\n((?:[ \t].*?(?:\n|$))*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)
    clean_text = clean_match.group(1).strip() if clean_match else ""

    fuzzy_sha = sha256(clean_text)

    new_front = re.sub(r'fuzzy_sha256\s*:\s*[^\n]+\n?', '', front_body)
    new_front = new_front.strip() + f"\nfuzzy_sha256: {fuzzy_sha}\n"

    new_content = front_start + new_front.strip() + "\n" + front_end + body

    if update:
        backup = filepath.with_suffix('.bak_fuzzy')
        backup.write_text(content, encoding='utf-8')
        filepath.write_text(new_content, encoding='utf-8')
        print(f"✅ fuzzy updated: {filepath.name}")
    else:
        print(f"DRY fuzzy: {filepath.name} → {fuzzy_sha[:12]}...")

    return True

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-d" in sys.argv
    base_dir = Path("_social-posts")
    for lang in ["nl", "en"]:
        for file in sorted((base_dir / lang).glob("day-*.md")):
            update_fuzzy(file, not dry_run)