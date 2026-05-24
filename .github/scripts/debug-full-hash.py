#!/usr/bin/env python3
"""
debug-full-hash.py
Toont exact wat er gebruikt wordt voor full_sha256 berekening + berekent de hash.
"""

import re
import hashlib
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def debug_file(file_path):
    content = file_path.read_text(encoding='utf-8')
    
    print(f"\n=== DEBUG: {file_path.name} ===")
    
    # Extract raw_markdown block
    match = re.search(r'raw_markdown:\s*\|\s*\n((?:.*?\n)+?)(?=\n\w+:\s|^\s*---|\Z)', content, re.MULTILINE)
    
    if not match:
        print("❌ Geen raw_markdown block gevonden!")
        return False
    
    raw_md = match.group(1).rstrip('\n')
    
    print("=== VOLLEDIGE RAW MARKDOWN (zoals gebruikt voor hash) ===")
    print(raw_md)
    print("\n=== LENGTE ===")
    print(f"{len(raw_md)} karakters")
    
    computed_hash = sha256(raw_md)
    print("\n=== BEREKENDE FULL SHA256 ===")
    print(computed_hash)
    
    # Check huidige waarde in frontmatter
    current_match = re.search(r'full_sha256:\s*"([^"]+)"', content)
    if current_match:
        current = current_match.group(1)
        print(f"\nHuidige full_sha256 in frontmatter: {current}")
        if current == computed_hash:
            print("✅ MATCH!")
        else:
            print("❌ GEEN MATCH (moet bijgewerkt worden)")
    else:
        print("❌ Geen full_sha256 in frontmatter")
    
    return computed_hash

def main():
    import sys
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if path.exists():
            debug_file(path)
        else:
            print("Bestand niet gevonden")
    else:
        # Test op dag-90
        debug_file(Path("_social-posts/nl/day-90-rvn.md"))

if __name__ == "__main__":
    main()