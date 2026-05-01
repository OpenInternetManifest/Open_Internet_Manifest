#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path

def escape_for_js(text):
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    return text

def update_clean_texts(file_path, cleaned_text):
    js_file = Path("static/js/official-clean-texts.js")
    js_file.parent.mkdir(parents=True, exist_ok=True)

    if not js_file.exists():
        js_file.write_text('// ==================== OFFICIAL CLEAN TEXTS ====================\n'
                           '// Gegenereerd op: ' + __import__('datetime').datetime.now().strftime('%Y-%m-%d') + '\n\n'
                           'window.officialCleanTexts = {\n};\n')

    content = js_file.read_text(encoding='utf-8')

    # Verwijder oude entry als die bestaat
    content = re.sub(rf'"{re.escape(file_path)}":\s*".*?",?\s*', '', content, flags=re.DOTALL)

    # Voeg nieuwe entry toe (vóór de laatste })
    new_entry = f'  "{file_path}": "{escape_for_js(cleaned_text)}",\n'
    content = re.sub(r'(\s*)\};', r'\1' + new_entry + r'\1};', content)

    js_file.write_text(content, encoding='utf-8')
    print(f"✅ Updated clean text for {file_path} in official-clean-texts.js")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update-clean-texts.py <file_path> <cleaned_text>")
        sys.exit(1)
    
    update_clean_texts(sys.argv[1], sys.argv[2])