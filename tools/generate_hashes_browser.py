#!/usr/bin/env python3
import sys
import hashlib
import re

if len(sys.argv) < 2:
    print("Usage: python3 fix-fuzzy-hash.py path/to/day-XX-rvn.md")
    sys.exit(1)

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the FIRST frontmatter block only (first --- ... ---)
match = re.search(r'^(---\s*.*?^---\s*)', content, re.DOTALL | re.MULTILINE)
if not match:
    print("Could not find frontmatter")
    sys.exit(1)

frontmatter_block = match.group(1)
body = content[match.end():].lstrip()   # remove leading whitespace/newlines

# Calculate fuzzy hash
def fuzzy_clean(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^>[ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*###*[ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*[0-9]+\.[ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*[-*+][ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\| ?', ' ', text)
    text = re.sub(r'^[-:| ]+$', '', text, flags=re.MULTILINE)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

fuzzy_text = fuzzy_clean(body)
fuzzy_hash = hashlib.sha256(fuzzy_text.encode('utf-8')).hexdigest()

print(f"Calculated fuzzy_sha256: {fuzzy_hash}")

# Clean frontmatter (remove old fuzzy lines)
clean_front = re.sub(r'^\s*fuzzy_sha256:.*\n?', '', frontmatter_block, flags=re.MULTILINE)

# Build final content - exactly one frontmatter block
new_content = clean_front.rstrip() + "\n" + f'fuzzy_sha256: "{fuzzy_hash}"\n---\n\n' + body

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ File fixed with clean single frontmatter!")
print("\nFirst 45 lines:")
print('\n'.join(new_content.splitlines()[:45]))