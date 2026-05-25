#!/usr/bin/env python3
"""
update-clean-texts.py - Correcte comma handling
"""

import sys
import re
import hashlib
from pathlib import Path

def escape_for_js(text):
    if not text:
        return ""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    return text

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 update-clean-texts.py <file_path> <cleaned_text>")
        sys.exit(1)

    file_path_str = sys.argv[1]
    cleaned_text = sys.argv[2]

    js_file = Path("static/js/official-clean-texts.js")
    
    if not js_file.exists():
        js_file.write_text("""// ==================== OFFICIAL FUZZY HASHES + CLEAN TEXTS ====================
// Auto generated - do not edit manually

window.officialFuzzyHashes = {};
window.officialCleanTexts = {};
""", encoding='utf-8')

    content = js_file.read_text(encoding='utf-8')

    # Verwijder oude entries voor dit bestand
    content = re.sub(rf'"{re.escape(file_path_str)}":\s*".*?",?\s*', '', content, flags=re.DOTALL)
    content = re.sub(rf'"[a-f0-9]{{64}}":\s*"{re.escape(file_path_str)}",?\s*', '', content, flags=re.DOTALL)

    fuzzy_hash = hashlib.sha256(cleaned_text.encode('utf-8')).hexdigest()

    new_fuzzy = f'  "{fuzzy_hash}": "{file_path_str}",\n'
    new_clean = f'  "{file_path_str}": "{escape_for_js(cleaned_text)}",\n'

    # Update FuzzyHashes
    content = re.sub(r'(window\.officialFuzzyHashes\s*=\s*\{[\s\S]*?)\s*\};', r'\1' + new_fuzzy + r'\1};', content, count=1)
    
    # Update CleanTexts
    content = re.sub(r'(window\.officialCleanTexts\s*=\s*\{[\s\S]*?)\s*\};', r'\1' + new_clean + r'\1};', content, count=1)

    js_file.write_text(content, encoding='utf-8')
    print(f"✅ Updated JS for {file_path_str} ({fuzzy_hash[:12]}...)")

if __name__ == "__main__":
    main()