#!/usr/bin/env python3
"""
update-clean-texts.py - Volledige rebuild (schoon en betrouwbaar)
"""

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

def rebuild_clean_texts():
    js_file = Path("static/js/official-clean-texts.js")
    fuzzy_hashes = {}
    clean_texts = {}

    print("🔄 Rebuilding official-clean-texts.js from all posts...")

    for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
        for file_path in sorted(Path(".").glob(pattern)):
            content = file_path.read_text(encoding='utf-8')

            # Prefer raw_markdown, fallback to body
            match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE | re.DOTALL)
            if match:
                raw_text = match.group(1).rstrip('\n')
            else:
                body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
                raw_text = body_match.group(1) if body_match else content

            clean_text = re.sub(r'\s+', ' ', raw_text.strip()).strip()
            fuzzy_hash = hashlib.sha256(clean_text.encode('utf-8')).hexdigest()
            web_path = str(file_path).replace('\\', '/')

            fuzzy_hashes[fuzzy_hash] = web_path
            clean_texts[web_path] = clean_text

    # Build clean JS
    js_content = """// ==================== OFFICIAL FUZZY HASHES + CLEAN TEXTS ====================
// Auto generated - do not edit manually

window.officialFuzzyHashes = {
"""

    for h, p in fuzzy_hashes.items():
        js_content += f'  "{h}": "{p}",\n'

    js_content = js_content.rstrip(',\n') + "\n};\n\nwindow.officialCleanTexts = {\n"

    for p, t in clean_texts.items():
        js_content += f'  "{p}": "{escape_for_js(t)}",\n'

    js_content = js_content.rstrip(',\n') + "\n};\n"

    js_file.write_text(js_content, encoding='utf-8')
    print(f"🎉 Clean rebuild completed with {len(fuzzy_hashes)} entries!")

if __name__ == "__main__":
    rebuild_clean_texts()