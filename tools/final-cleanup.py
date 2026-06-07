#!/usr/bin/env python3
# tools/final-cleanup.py - Laatste grote schoonmaak

import sys
import re
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from fuzzy_clean import fuzzy_clean
import hashlib
import textwrap

def final_fix(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract raw_markdown (meest betrouwbaar)
    raw_match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\s*\w+\s*:|\n---|\Z)', content, re.DOTALL)
    raw_markdown = raw_match.group(1).strip() if raw_match else ""

    clean_text = fuzzy_clean(raw_markdown)

    # Verwijder ALLE clean_text uit de body (inclusief duplicaten)
    content = re.sub(r'clean_text:\s*[\s\S]*?(?=\n---|\Z)', '', content, flags=re.MULTILINE)

    # Bouw perfecte frontmatter
    new_front = "---\n"
    # Houd bestaande metadata
    for key in ['layout', 'lang', 'day', 'rvn_title', 'rvn_teaser', 'donation_link', 'donation_text', 'git_commit_hash', 'git_commit_url', 'git_commit_date']:
        m = re.search(rf'{key}\s*:\s*(.+?)(?=\n\s*\w+\s*:|\n---|\Z)', content)
        if m:
            val = m.group(1).strip().strip('"')
            new_front += f"{key}: {val}\n" if not val.startswith('"') else f'{key}: "{val}"\n'

    new_front += f"raw_markdown: |\n{textwrap.indent(raw_markdown, '  ')}\n\n"
    new_front += f"clean_text: |-\n{textwrap.indent(clean_text, '  ')}\n\n"
    new_front += f"full_sha256: {hashlib.sha256(raw_markdown.encode()).hexdigest()}\n"
    new_front += f"fuzzy_sha256: {hashlib.sha256(clean_text.encode()).hexdigest()}\n"
    new_front += "---\n"

    # Haal oude frontmatter weg en vervang
    new_content = re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n', new_front, content, flags=re.MULTILINE)

    if dry_run:
        print(f"DRY-RUN: Would fix {filepath.name} ({len(clean_text)} chars)")
        return True
    else:
        backup = filepath.with_suffix('.bak_final')
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed: {filepath.name}")
        return True

if __name__ == "__main__":
    dry_run = "--update" not in sys.argv

    if dry_run:
        print("🚀 FINAL DRY RUN\n")
    else:
        print("🔥 FINAL LIVE CLEANUP\n")

    base = Path("_social-posts")
    fixed = 0

    for lang in ["nl", "en"]:
        for file in sorted((base / lang).glob("day-*.md")):
            if final_fix(file, dry_run):
                fixed += 1

    print(f"\nKlaar! {fixed} bestanden verwerkt")
    if dry_run:
        print("\nRun dit om écht alles schoon te maken:")
        print("python3 tools/final-cleanup.py --update")