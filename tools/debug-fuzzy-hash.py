#!/usr/bin/env python3
# tools/debug-fuzzy-hash.py - Volledige clean_text debug + betere stripping

import sys
import re
import hashlib
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def debug_fuzzy(filepath):
    filepath = Path(filepath)
    content = filepath.read_text(encoding='utf-8')

    match = re.search(r'clean_text\s*:\s*\|-?\s*\n([\s\S]*?)(?=\n\w+\s*:|\n---\s*$|\Z)', content, re.DOTALL)
    if not match:
        print(f"❌ Geen clean_text gevonden in {filepath.name}")
        return

    clean_text = match.group(1).strip()

    # Extra agressieve whitespace cleanup
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    fuzzy_sha = sha256(clean_text)

    print(f"\n=== FULL DEBUG: {filepath.name} ===")
    print(f"Clean text length : {len(clean_text)} karakters\n")

    print("--- VOLLEDIGE CLEAN_TEXT (first 1500) ---")
    print(clean_text[:60000])
    

    print("\n" + "="*90)
    print("fuzzy_sha256 :", fuzzy_sha)
    print("="*90)

    if "--update" in sys.argv:
        new_content = re.sub(
            r'fuzzy_sha256\s*:\s*[^\n\r]+',
            f'fuzzy_sha256: {fuzzy_sha}',
            content
        )
        backup = filepath.with_suffix('.bak_fuzzy_debug')
        backup.write_text(content, encoding='utf-8')
        filepath.write_text(new_content, encoding='utf-8')
        print(f"✅ fuzzy_sha256 bijgewerkt + backup gemaakt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/debug-fuzzy-hash.py <bestand.md> [--update]")
        sys.exit(1)

    debug_fuzzy(sys.argv[1])