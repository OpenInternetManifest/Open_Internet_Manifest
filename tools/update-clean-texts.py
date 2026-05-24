#!/usr/bin/env python3
import sys
from hashlib import sha256
from pathlib import Path

file_path = sys.argv[1]
cleaned_text = sys.argv[2]

fuzzy_sha256 = sha256(cleaned_text.encode('utf-8')).hexdigest()

# Frontmatter
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'fuzzy_sha256:' in content:
    content = re.sub(r'fuzzy_sha256:\s*["\']?[^"\']*["\']?', f'fuzzy_sha256: "{fuzzy_sha256}"', content)
else:
    content = re.sub(r'(\n---\s*\n)', rf'\nfuzzy_sha256: "{fuzzy_sha256}"\n', content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# JS append
js_file = Path("static/js/official-clean-texts.js")
js_content = js_file.read_text(encoding='utf-8')

# Hash
if fuzzy_sha256 not in js_content:
    js_content = js_content.replace(
        'officialFuzzyHashes = {};',
        f'officialFuzzyHashes = {{\n  "{fuzzy_sha256}": "{file_path}",\n}};'
    )

# Clean text
if str(file_path) not in js_content:
    escaped = cleaned_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    js_content = js_content.replace(
        'officialCleanTexts = {};',
        f'officialCleanTexts = {{\n  "{file_path}": "{escaped}",\n}};'
    )

js_file.write_text(js_content, encoding='utf-8')
print(f"Added {file_path}")