#!/usr/bin/env python3
import re
import hashlib
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def update_file(file_path):
    content = file_path.read_text(encoding='utf-8')
    original = content

    # Extract raw_markdown block (alles na "raw_markdown: |" tot volgende top-level key of einde)
    match = re.search(r'raw_markdown:\s*\|\s*\n((?:.*?\n)+?)(?=\n\w+:\s|^\s*---|\Z)', content, re.MULTILINE)
    if not match:
        print(f"⚠️  Geen raw_markdown: {file_path.name}")
        return False

    raw_md = match.group(1).rstrip('\n')
    new_hash = sha256(raw_md)

    # Update full_sha256
    if 'full_sha256:' in content:
        content = re.sub(r'full_sha256:\s*".*?"', f'full_sha256: "{new_hash}"', content)
    else:
        # Insert na fuzzy_sha256
        content = re.sub(
            r'(fuzzy_sha256:.*?\n)',
            rf'\1full_sha256: "{new_hash}"\n',
            content
        )

    if content != original:
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ {file_path.name} → {new_hash[:12]}...")
        return True
    return False

def main():
    print("🚀 Updating full_sha256 from raw_markdown...\n")
    updated = 0
    for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
        for f in sorted(Path(".").glob(pattern)):
            if update_file(f):
                updated += 1
    print(f"\n🎉 Klaar! {updated} bestanden bijgewerkt.")

if __name__ == "__main__":
    main()