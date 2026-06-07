#!/usr/bin/env python3
# tools/fix-hr-in-body.py - Fix alleen --- in body

import sys
import re
from pathlib import Path

def fix_hr_in_body(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Vind waar de frontmatter eindigt (tweede ---)
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False  # geen geldige frontmatter

    frontmatter = parts[0] + '---' + parts[1] + '---'
    body = parts[2]

    # Vervang alleen losse --- in de body
    fixed_body = re.sub(r'^\s*---\s*$', '————————————', body, flags=re.MULTILINE)

    if fixed_body != body:
        new_content = frontmatter + fixed_body

        if dry_run:
            print(f"DRY-RUN: Would fix HR in body of {filepath.name}")
            return True
        else:
            backup = filepath.with_suffix('.bak_hr')
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(original)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ HR fixed in body: {filepath.name}")
            return True
    return False

if __name__ == "__main__":
    dry_run = "--update" not in sys.argv

    if dry_run:
        print("🚀 DRY RUN - fix --- in body\n")
    else:
        print("🔥 LIVE HR FIX\n")

    base = Path("_social-posts")
    fixed = 0
    total = 0

    for lang in ["nl", "en"]:
        for file in sorted((base / lang).glob("day-*.md")):
            total += 1
            if fix_hr_in_body(file, dry_run):
                fixed += 1

    print(f"\nKlaar! {fixed}/{total} bestanden hadden --- in body")
    if dry_run:
        print("\nRun dit om echt te fixen:")
        print("python3 tools/fix-hr-in-body.py --update")