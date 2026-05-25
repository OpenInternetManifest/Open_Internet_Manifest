#!/usr/bin/env python3
"""
debug-raw-hash.py - Toont exact wat het script gebruikt voor full_sha256
"""

import re
import hashlib
import sys
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main(file_path):
    file = Path(file_path)
    content = file.read_text(encoding='utf-8')

    print(f"=== DEBUG RAW HASH for {file.name} ===")

    # Extract raw_markdown block
    match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE | re.DOTALL)
    
    if not match:
        print("❌ Geen raw_markdown block gevonden!")
        return

    raw_md = match.group(1).rstrip('\n')

    print(f"\n📏 Lengte raw_md block: {len(raw_md)} karakters")
    print("\n📋 EXACTE RAW MARKDOWN (zoals in script gebruikt):")
    print(repr(raw_md))
    print("\n" + "="*100)
    print(raw_md)
    print("="*100)

    computed_hash = sha256(raw_md)
    print(f"\n🔢 HASH berekend door script:")
    print(computed_hash)

    print("\n💡 Kopieer de 'EXACTE RAW MARKDOWN' hierboven (tussen de = lijnen) en plak in een online SHA256 tool.")
    print("Vergelijk of het dezelfde hash geeft als het script.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 debug-raw-hash.py <file>")
        sys.exit(1)
    main(sys.argv[1])