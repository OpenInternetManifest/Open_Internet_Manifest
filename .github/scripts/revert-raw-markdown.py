#!/usr/bin/env python3
"""
revert-raw-markdown.py - Verwijdert raw_markdown die buiten frontmatter staat
"""

import re
from pathlib import Path

def revert_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verwijder raw_markdown blok dat na de tweede --- staat
    content = re.sub(r'\nraw_markdown: \|[\s\S]*?(?=\n---\s*\n|\Z)', '', content, flags=re.MULTILINE)

    # Verwijder eventuele dubbele ---
    content = re.sub(r'\n---\s*\n---', '\n---', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Reverted: {file_path.name}")

def main():
    base = Path(".")
    patterns = ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]

    for pattern in patterns:
        for file in sorted(base.glob(pattern)):
            revert_file(file)

    print("\n🎉 Revert klaar.")

if __name__ == "__main__":
    main()
