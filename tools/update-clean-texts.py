#!/usr/bin/env python3
"""
update-clean-texts.py - Volledige rebuild versie (meest robuust)
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

def rebuild_clean_texts():
    """Volledig herbouwen van official-clean-texts.js uit alle posts"""
    js_file = Path("static/js/official-clean-texts.js")
    js_file.parent.mkdir(parents=True, exist_ok=True)

    fuzzy_hashes = {}
    clean_texts = {}

    patterns = ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]

    for pattern in patterns:
        for file_path in sorted(Path(".").glob(pattern)):
            content = file_path.read_text(encoding='utf-8')
            
            # Extract raw_markdown als aanwezig, anders body
            match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE)
            if match:
                raw_text = match.group(1).rstrip('\n')
            else:
                # fallback body
                body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE)
                raw_text = body_match.group(1) if body_match else content

            clean_text = re.sub(r'\s+', ' ', raw_text.strip()).strip()
            fuzzy_hash = hashlib.sha256(clean_text.encode('utf-8')).hexdigest()

            web_path = str(file_path).replace('\\', '/')

            fuzzy_hashes[fuzzy_hash] = web_path
            clean_texts[web_path] = clean_text

            print(f"✓ {file_path.name}")

    # Bouw JS bestand op
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
    print(f"\n🎉 Volledig herbouwd met {len(fuzzy_hashes)} entries!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single file mode (voor calculate-hashes.sh)
        file_path = sys.argv[1]
        # Voor nu gewoon full rebuild (simpelst en veiligst)
        rebuild_clean_texts()
    else:
        rebuild_clean_texts()