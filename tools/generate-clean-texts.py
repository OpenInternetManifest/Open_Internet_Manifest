#!/usr/bin/env python3
"""
generate-clean-texts.py - Gebruikt raw_markdown voor consistente hashes + clean texts
"""

import re
import unicodedata
from hashlib import sha256
from pathlib import Path

def fuzzy_clean(text):
    if not text:
        return ""

    t = unicodedata.normalize('NFKC', text)

    # Markdown stripping (eenvoudig en consistent)
    t = re.sub(r'\*\*(.*?)\*\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'__(.*?)__', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'\*(.*?)\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'_(.*?)_', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'^#{1,6}\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'^>\s*', '', t, flags=re.MULTILINE)
    t = re.sub(r'^\s*[-*+]\s+', ' ', t, flags=re.MULTILINE)
    t = re.sub(r'^\s*\d+\.\s+', ' ', t, flags=re.MULTILINE)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'!\[.*?\]\(.*?\)', '', t)
    t = re.sub(r'`([^`]+)`', r'\1', t)
    t = re.sub(r'^-{3,}\s*$', '', t, flags=re.MULTILINE)
    t = re.sub(r'<[^>]+>', '', t)

    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def main():
    base_dir = Path(".")
    patterns = ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]

    print("🔄 Generating official-clean-texts.js using raw_markdown...\n")

    fuzzy_hashes = {}
    clean_texts = {}

    for pattern in patterns:
        for file_path in sorted(base_dir.glob(pattern)):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Haal raw_markdown uit frontmatter
            match = re.search(r'raw_markdown:\s*\|\s*\n((?:  .*\n)*)', content, re.MULTILINE)
            if not match:
                print(f"✗ Geen raw_markdown in {file_path.name} → overslaan")
                continue

            raw_markdown = match.group(1).replace('  ', '', 1).rstrip()

            clean_text = fuzzy_clean(raw_markdown)
            web_path = str(file_path).replace('\\', '/')

            fuzzy_sha = sha256(clean_text.encode('utf-8')).hexdigest()

            fuzzy_hashes[fuzzy_sha] = web_path
            clean_texts[web_path] = clean_text

            print(f"✓ {file_path.name} → {fuzzy_sha[:12]}...")

    # Schrijf JS bestand
    js_output = '''// ==================== OFFICIAL FUZZY HASHES + CLEAN TEXTS ====================
// Auto generated using raw_markdown - do not edit manually

window.officialFuzzyHashes = {
'''

    for h, p in fuzzy_hashes.items():
        js_output += f'  "{h}": "{p}",\n'

    js_output = js_output.rstrip(',\n') + "\n};\n\nwindow.officialCleanTexts = {\n"

    for p, t in clean_texts.items():
        escaped = t.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        js_output += f'  "{p}": "{escaped}",\n'

    js_output = js_output.rstrip(',\n') + "\n};\n"

    output_file = Path("static/js/official-clean-texts.js")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(js_output, encoding='utf-8')

    print(f"\n🎉 Klaar! {output_file} gegenereerd met {len(fuzzy_hashes)} entries.")

if __name__ == "__main__":
    main()