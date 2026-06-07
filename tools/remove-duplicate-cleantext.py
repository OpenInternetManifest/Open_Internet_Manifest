#!/usr/bin/env python3
# tools/remove-duplicate-cleantext.py - Verwijder clean_text rommel uit body

import sys
import re
from pathlib import Path

def clean_body(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # Verwijder alle clean_text blokken uit de body
    content = re.sub(r'clean_text:\s*[\s\S]*?(?=\n---|\Z)', '', content, flags=re.MULTILINE)
    content = re.sub(r'full_sha256:.*\n?fuzzy_sha256:.*\n?', '', content, flags=re.MULTILINE)

    if len(content) < original_len - 50:   # er is iets verwijderd
        if dry_run:
            print(f"DRY-RUN: Would clean body of {filepath.name}")
            return True
        else:
            backup = filepath.with_suffix('.bak_body')
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(content)   # oude versie als backup
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Body cleaned: {filepath.name}")
            return True
    return False

if __name__ == "__main__":
    dry_run = "--update" not in sys.argv

    if dry_run:
        print("🚀 DRY RUN - body cleanup\n")
    else:
        print("🔥 LIVE BODY CLEANUP\n")

    base = Path("_social-posts")
    count = 0

    for lang in ["nl", "en"]:
        for file in sorted((base / lang).glob("day-*.md")):
            if clean_body(file, dry_run):
                count += 1

    print(f"\nKlaar! {count} bestanden hadden body-opruiming nodig")
    if dry_run:
        print("\nRun dit om echt op te ruimen:")
        print("python3 tools/remove-duplicate-cleantext.py --update")