#!/usr/bin/env python3
# tools/restore-missing-clean-text.py - Herstel ALLE corrupte/korte clean_text

import sys
import re
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from fuzzy_clean import fuzzy_clean

def needs_restore(content):
    """Herstel als clean_text ontbreekt, te kort is, of hashes bevat"""
    if 'clean_text:' not in content:
        return True
    
    match = re.search(r'clean_text\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\s*\w+\s*:|\n---|\Z)', content, re.DOTALL)
    if not match:
        return True
    
    ct = match.group(1).strip()
    if len(ct) < 300:                    # was 100 → nu ruimer
        return True
    if 'full_sha256' in ct or 'fuzzy_sha256' in ct:   # corrupt
        return True
    return False

def update_file(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not needs_restore(content):
        return False

    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content)
    if not match:
        return False

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)
    body = match.group(4)

    raw_match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\s*\w+\s*:|\n---|\Z)', front_body, re.DOTALL)
    if not raw_match:
        return False

    raw_markdown = raw_match.group(1).strip()
    clean_text = fuzzy_clean(raw_markdown)

    # Verwijder oude clean_text
    new_front_body = re.sub(r'clean_text\s*:\s*[\s\S]*?(?=\n\s*\w+\s*:|\n---|\Z)', '', front_body, flags=re.DOTALL).strip()

    if new_front_body:
        new_front_body += "\n"
    new_front_body += f"clean_text: |-\n  {clean_text.replace('\n', '\n  ')}"

    new_content = front_start + new_front_body + "\n" + front_end + body

    if dry_run:
        print(f"DRY-RUN: Would restore clean_text in {filepath.name} ({len(clean_text)} chars)")
        return True
    else:
        backup = filepath.with_suffix('.bak_restore2')
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Restored: {filepath.name} ({len(clean_text)} chars)")
        return True

if __name__ == "__main__":
    dry_run = "--update" not in sys.argv

    if dry_run:
        print("🚀 DRY RUN - Herstel van corrupte/korte clean_text\n")
    else:
        print("🔥 LIVE RESTORE\n")

    base = Path("_social-posts")
    total = 0
    restored = 0

    for lang in ["nl", "en"]:
        dir_path = base / lang
        if not dir_path.exists():
            continue
        print(f"\n=== {lang.upper()} ===")
        for file in sorted(dir_path.glob("day-*.md")):
            total += 1
            if update_file(file, dry_run):
                restored += 1

    print(f"\nKlaar! {restored}/{total} bestanden hersteld")
    if dry_run:
        print("\nRun dit om echt te herstellen:")
        print("python3 tools/restore-missing-clean-text.py --update")