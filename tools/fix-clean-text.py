#!/usr/bin/env python3
# tools/fix-clean-text.py - Veilige clean_text → één regel

import sys
import re
import shutil
from pathlib import Path

def needs_fixing(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Zoek clean_text block
    match = re.search(r'clean_text\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\w+\s*:|\n---|\Z)', content, re.DOTALL)
    if match:
        clean_text = match.group(1).strip()
        return '\n' in clean_text or len(clean_text.splitlines()) > 1
    return False

def fix_file(filepath, dry_run=True):
    filepath = Path(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if dry_run and not needs_fixing(filepath):
        return False

    # Backup
    if not dry_run:
        backup = filepath.with_suffix('.bak_cleantext')
        shutil.copy2(filepath, backup)

    # Vervang multi-line clean_text door single line
    def replace_clean(match):
        clean_text = match.group(1).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        return f"clean_text: {clean_text}"

    new_content = re.sub(
        r'clean_text\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\w+\s*:|\n---|\Z)',
        replace_clean,
        content,
        flags=re.DOTALL
    )

    if dry_run:
        print(f"Would fix → {filepath.name}")
        return True
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Gefixt → {filepath.name}")
        return True


if __name__ == "__main__":
    update = "--update" in sys.argv
    files = [arg for arg in sys.argv[1:] if arg != "--update"]

    if not files:
        print("Gebruik: python3 tools/fix-clean-text.py <bestand.md> [--update]")
        sys.exit(1)

    to_fix = 0
    fixed = 0

    for f in files:
        if fix_file(f, dry_run=not update):
            to_fix += 1
            if update:
                fixed += 1

    print("\n" + "="*65)
    if update:
        print(f"✅ KLAAR — {fixed} bestanden gefixt")
    else:
        print(f"DRY-RUN — {to_fix} bestanden zouden worden gefixt")
    print("="*65)