#!/usr/bin/env python3
import sys
import hashlib
import re
from pathlib import Path
from datetime import datetime

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

def fix_file(file_path, log_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'^\s*fuzzy_sha256:.*\n?', '', content, flags=re.MULTILINE)

    match = re.search(r'^(---\s*[\s\S]*?^---\s*)', content, re.MULTILINE)
    if not match:
        log_file.write(f"[{datetime.now()}] ⚠️  Could not find frontmatter in {file_path.name}\n")
        print(f"⚠️  Could not find frontmatter in {file_path.name}")
        return False

    frontmatter = match.group(1)
    body = content[match.end():].lstrip()

    fuzzy_text = fuzzy_clean(body)
    fuzzy_hash = hashlib.sha256(fuzzy_text.encode('utf-8')).hexdigest()

    if f'fuzzy_sha256: "{fuzzy_hash}"' in frontmatter:
        print(f"✅ {file_path.name} already up to date")
        log_file.write(f"[{datetime.now()}] ✅ {file_path.name} already up to date\n")
        return True

    lines = frontmatter.strip().splitlines()
    if lines and lines[-1].strip() == '---':
        lines.pop()

    new_frontmatter = '\n'.join(lines) + f'\nfuzzy_sha256: "{fuzzy_hash}"\n---'
    new_content = new_frontmatter + '\n' + body

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Updated {file_path.name}")
    log_file.write(f"[{datetime.now()}] ✅ Updated {file_path.name} → fuzzy_sha256: {fuzzy_hash}\n")
    return True

# ==================== BATCH RUN ====================
if __name__ == "__main__":
    base_dir = Path(".")
    patterns = ["_social-posts/nl/day-*-rvn.md", "_social-posts/en/day-*-rvn.md"]

    log_path = Path("fuzzy-fix-log.txt")
    updated = 0
    total = 0

    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n=== Fuzzy Hash Fix Run - {datetime.now()} ===\n")

        for pattern in patterns:
            for file_path in sorted(base_dir.glob(pattern)):
                total += 1
                if fix_file(file_path, log_file):
                    updated += 1

        log_file.write(f"Summary: {updated}/{total} files processed\n")

    print(f"\n🎉 Klaar! {updated}/{total} bestanden verwerkt.")
    print(f"📄 Logbestand aangemaakt: fuzzy-fix-log.txt")