#!/usr/bin/env python3
# tools/update-fuzzy-hash.py - Herberekent fuzzy_sha256 op basis van clean_text

import sys
import re
import hashlib
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def update_fuzzy(filepath, update=False):
    filepath = Path(filepath)
    content = filepath.read_text(encoding='utf-8')

    # Extract clean_text (multi-line met |- of |)
    match = re.search(r'clean_text\s*:\s*\|-?\s*\n([\s\S]*?)(?=\n\w+\s*:|\n---\s*$|\Z)', content, re.DOTALL)
    if not match:
        print(f"⚠️  Geen clean_text gevonden: {filepath.name}")
        return False

    clean_text = match.group(1).strip()
    fuzzy_sha = sha256(clean_text)

    if not update:
        print(f"DRY-RUN → {filepath.name} | fuzzy: {fuzzy_sha[:16]}...")
        return True

    # Backup + update
    backup = filepath.with_suffix('.bak_fuzzy')
    backup.write_text(content, encoding='utf-8')

    # Vervang oude fuzzy_sha256
    new_content = re.sub(
        r'fuzzy_sha256\s*:\s*[^\n\r]+',
        f'fuzzy_sha256: {fuzzy_sha}',
        content
    )

    filepath.write_text(new_content, encoding='utf-8')
    print(f"✅ fuzzy_sha256 bijgewerkt: {filepath.name}")
    return True


if __name__ == "__main__":
    update_mode = "--update" in sys.argv
    files = [arg for arg in sys.argv[1:] if arg != "--update"]

    if not files:
        # Bulk mode
        print("🔄 Bulk fuzzy_sha256 update started...\n")
        total = 0
        for lang in ["nl", "en"]:
            for file in sorted(Path(f"_social-posts/{lang}").glob("*.md")):
                if update_fuzzy(file, update_mode):
                    total += 1
        print(f"\n🎉 Klaar! {total} bestanden verwerkt.")
    else:
        # Single file(s)
        for f in files:
            update_fuzzy(f, update_mode)