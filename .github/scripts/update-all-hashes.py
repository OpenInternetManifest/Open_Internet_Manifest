#!/usr/bin/env python3
"""
update-all-hashes.py - Voegt zowel fuzzy als full_sha256 toe (definitief)
"""

import re
from hashlib import sha256
from pathlib import Path

def fuzzy_clean(text):
    if not text:
        return ""
    t = re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n', '', text, flags=re.MULTILINE)
    t = re.sub(r'\*\*(.*?)\*\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'__(.*?)__', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'\*(.*?)\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'_(.*?)_', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'^#{1,6}\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'^>\s*', '', t, flags=re.MULTILINE)
    t = re.sub(r'^\s*[-*+]\s+', ' ', t, flags=re.MULTILINE)
    t = re.sub(r'^\s*\d+\.\s+', ' ', t, flags=re.MULTILINE)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'!\[.*?\]\(.*?\)', '', t)
    t = re.sub(r'`([^`]+)`', r'\1', t)
    t = re.sub(r'^-{3,}\s*$', '', t, flags=re.MULTILINE)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Haal raw_markdown op
    match = re.search(r'raw_markdown:\s*\|\s*\n((?:  .*\n)*)', content, re.MULTILINE)
    if not match:
        print(f"✗ Geen raw_markdown: {file_path.name}")
        return False

    raw_markdown = match.group(1).replace('  ', '', 1).rstrip()

    fuzzy_sha256 = sha256(fuzzy_clean(raw_markdown).encode('utf-8')).hexdigest()
    full_sha256 = sha256(raw_markdown.encode('utf-8')).hexdigest()

    # Update fuzzy_sha256
    content = re.sub(r'fuzzy_sha256:\s*["\']?[^"\']*["\']?', f'fuzzy_sha256: "{fuzzy_sha256}"', content)

    # Update full_sha256
    content = re.sub(r'full_sha256:\s*["\']?[^"\']*["\']?', f'full_sha256: "{full_sha256}"', content)

    # Voeg toe als ze nog niet bestaan
    if 'fuzzy_sha256:' not in content:
        content = re.sub(r'(\n---\s*\n)', rf'\nfuzzy_sha256: "{fuzzy_sha256}"\nfull_sha256: "{full_sha256}"\1', content, count=1)
    elif 'full_sha256:' not in content:
        content = re.sub(r'(fuzzy_sha256: "[^"]+")', rf'\1\nfull_sha256: "{full_sha256}"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated {file_path.name}")
    print(f"   fuzzy: {fuzzy_sha256[:12]}...")
    print(f"   full : {full_sha256[:12]}...")
    return True

def main():
    base = Path(".")
    patterns = ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]

    updated = 0
    for pattern in patterns:
        for file in sorted(base.glob(pattern)):
            if update_file(file):
                updated += 1

    print(f"\n🎉 Klaar! {updated} bestanden bijgewerkt.")

if __name__ == "__main__":
    main()