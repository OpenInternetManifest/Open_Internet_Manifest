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

# Remove ALL existing fuzzy_sha256 lines anywhere in the file
content = re.sub(r'^\s*fuzzy_sha256:.*\n?', '', content, flags=re.MULTILINE)

# Find the frontmatter (first --- ... ---)
match = re.search(r'^(---\s*[\s\S]*?^---\s*)', content, re.MULTILINE)
if not match:
    print("Could not find frontmatter")
    sys.exit(1)

frontmatter = match.group(1)
body = content[match.end():].lstrip()

# Calculate fuzzy hash — safe version, matching debug-live-hashes.sh
def fuzzy_clean(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^>[ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*###*[ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*[0-9]+\.[ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*[-*+][ \t]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[ \t]*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\| ?', ' ', text)
    text = re.sub(r' \|', ' ', text)
    text = re.sub(r'^[-:| ]+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^--$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---$', '', text, flags=re.MULTILINE)
    text = text.lower()
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()
    return text

fuzzy_text = fuzzy_clean(body)
fuzzy_hash = hashlib.sha256(fuzzy_text.encode('utf-8')).hexdigest()

print(f"Calculated fuzzy_sha256: {fuzzy_hash}")
print("\n=== FULL FUZZY TEXT (complete) ===")
print(fuzzy_text)                                   # <--- Volledige tekst
print("\n=== LENGTH ===")
print(len(fuzzy_text), "characters")

# Insert fuzzy_sha256 inside frontmatter
lines = frontmatter.strip().splitlines()
if lines and lines[-1].strip() == '---':
    lines.pop()

new_frontmatter = '\n'.join(lines) + f'\nfuzzy_sha256: "{fuzzy_hash}"\n---'

new_content = new_frontmatter + '\n' + body

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n✅ File updated successfully.")
print("First 45 lines of new file:")
print('\n'.join(new_content.splitlines()[:45]))