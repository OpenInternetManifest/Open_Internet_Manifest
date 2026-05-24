#!/usr/bin/env python3
"""
test-update-hashes.py - Test op 1 specifiek bestand
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

def update_single_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'raw_markdown:\s*\|\s*\n((?:  .*\n)*)', content, re.MULTILINE)
    if not match:
        print(f"✗ Geen raw_markdown gevonden in {file_path.name}")
        return

    raw_markdown = match.group(1).replace('  ', '', 1).rstrip()

    fuzzy_sha256 = sha256(fuzzy_clean(raw_markdown).encode('utf-8')).hexdigest()
    full_sha256 = sha256(raw_markdown.encode('utf-8')).hexdigest()

    # Update frontmatter
    if 'fuzzy_sha256:' in content:
        content = re.sub(r'fuzzy_sha256:\s*["\']?[^"\']*["\']?', f'fuzzy_sha256: "{fuzzy_sha256}"', content)
    else:
        content = re.sub(r'(\n---\s*\n)', rf'\nfuzzy_sha256: "{fuzzy_sha256}"\n', content, count=1)

    if 'full_sha256:' in content:
        content = re.sub(r'full_sha256:\s*["\']?[^"\']*["\']?', f'full_sha256: "{full_sha256}"', content)
    else:
        content = re.sub(r'(fuzzy_sha256: "[^"]+")', rf'\1\nfull_sha256: "{full_sha256}"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated: {file_path.name}")
    print(f"   fuzzy_sha256: {fuzzy_sha256}")
    print(f"   full_sha256 : {full_sha256}")

if __name__ == "__main__":
    test_file = "_social-posts/nl/day-89-rvn.md"
    update_single_file(test_file)
