#!/usr/bin/env python3
# tools/update-clean-texts.py - Update zowel frontmatter als official-clean-texts.js

import sys
import re
from hashlib import sha256
from pathlib import Path

def escape_for_js(text):
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    return text

def update_file(file_path, cleaned_text):
    # Bereken hash
    fuzzy_sha256 = sha256(cleaned_text.encode('utf-8')).hexdigest()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update of voeg fuzzy_sha256 toe in frontmatter
    if 'fuzzy_sha256:' in content:
        content = re.sub(
            r'(fuzzy_sha256:\s*["\']?)[^"\']*',
            f'fuzzy_sha256: "{fuzzy_sha256}"',
            content
        )
    else:
        # Voeg toe na de eerste ---
        content = re.sub(
            r'^(---\s*\n)(.*?)(\n---\s*\n)',
            rf'\1\2fuzzy_sha256: "{fuzzy_sha256}"\n\3',
            content,
            flags=re.DOTALL
        )

    # Schrijf .md bestand terug
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Frontmatter updated: fuzzy_sha256 = {fuzzy_sha256}")

    # Update official-clean-texts.js
    js_file = Path("static/js/official-clean-texts.js")
    js_file.parent.mkdir(parents=True, exist_ok=True)

    if not js_file.exists():
        js_file.write_text('// ==================== OFFICIAL CLEAN TEXTS ====================\n'
                           'window.officialCleanTexts = {};\n')

    js_content = js_file.read_text(encoding='utf-8')

    # Verwijder oude entry
    js_content = re.sub(rf'"{re.escape(str(file_path))}":\s*".*?",?\s*', '', js_content, flags=re.DOTALL)

    # Voeg nieuwe toe
    new_entry = f'  "{file_path}": "{escape_for_js(cleaned_text)}",\n'
    js_content = re.sub(r'(\s*)\};', r'\1' + new_entry + r'\1};', js_content)

    js_file.write_text(js_content, encoding='utf-8')
    print(f"✅ Updated clean text in official-clean-texts.js")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 update-clean-texts.py <file.md> <cleaned_text>")
        sys.exit(1)
    
    update_file(sys.argv[1], sys.argv[2])