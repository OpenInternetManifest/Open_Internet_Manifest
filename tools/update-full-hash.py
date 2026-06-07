#!/usr/bin/env python3
# tools/update-full-hash.py

import sys
import re
import hashlib
import textwrap
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def update_full(filepath, update=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content)
    if not match:
        return False

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)
    body = match.group(4)

    raw_match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)
    raw_markdown = textwrap.dedent(raw_match.group(1)).strip() if raw_match else ""

    full_sha = sha256(raw_markdown)

    new_front = re.sub(r'full_sha256\s*:\s*[^\n]+\n?', '', front_body)
    new_front = new_front.strip() + f"\nfull_sha256: {full_sha}\n"

    new_content = front_start + new_front.strip() + "\n" + front_end + body

    if update:
        backup = filepath.with_suffix('.bak_full')
        backup.write_text(content, encoding='utf-8')
        filepath.write_text(new_content, encoding='utf-8')
        print(f"✅ full updated: {filepath.name}")
    else:
        print(f"DRY full: {filepath.name} → {full_sha[:12]}...")

    return True

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-d" in sys.argv
    base_dir = Path("_social-posts")
    for lang in ["nl", "en"]:
        for file in sorted((base_dir / lang).glob("day-*.md")):
            update_full(file, not dry_run)