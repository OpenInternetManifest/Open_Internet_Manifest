#!/usr/bin/env python3
# tools/update-full-hash.py - Robuuste full_sha256 update op basis van raw_markdown

import sys
import re
import hashlib
import textwrap
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def extract_raw_markdown(content):
    """Extract raw_markdown block"""
    match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n([\s\S]*?)(?=\n\w+\s*:|\n---\s*$|\Z)', content, re.DOTALL)
    if match:
        return textwrap.dedent(match.group(1)).strip()
    return ""

def update_full(filepath, update=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_markdown = extract_raw_markdown(content)
    if not raw_markdown:
        print(f"❌ Geen raw_markdown gevonden: {filepath.name}")
        return False

    full_sha = sha256(raw_markdown)

    if not update:
        print(f"Would update → {filepath.name} | length: {len(raw_markdown)} | sha: {full_sha[:12]}...")
        return True

    # Backup + update
    backup = filepath.with_suffix('.bak_full')
    backup.write_text(content, encoding='utf-8')

    # Vervang bestaande full_sha256
    new_content = re.sub(
        r'full_sha256\s*:\s*[^\n\r]+',
        f'full_sha256: {full_sha}',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Updated full_sha256 → {filepath.name}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/update-full-hash.py <bestand.md> [--update]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    update = "--update" in sys.argv
    update_full(filepath, update)