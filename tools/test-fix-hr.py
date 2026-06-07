#!/usr/bin/env python3
# tools/test-fix-hr.py - Test HR fix op 1 bestand

import sys
import re
from pathlib import Path

def test_fix_hr(filepath, update=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Vind frontmatter + body
    parts = content.split('---', 2)
    if len(parts) < 3:
        print("Geen geldige frontmatter")
        return

    front = parts[0] + '---' + parts[1] + '---'
    body = parts[2]

    # Fix alleen in body
    fixed_body = re.sub(r'^\s*---\s*$', '————————————', body, flags=re.MULTILINE)

    new_content = front + fixed_body

    print(f"\n=== TEST OP {filepath.name} ===")
    print("Aantal --- vervangen in body:", fixed_body.count('————————————') - body.count('————————————'))

    if not update:
        print("\n--- EERSTE 100 chars van nieuwe body ---")
        print(fixed_body[:100] + "...")
        return

    # Update
    backup = filepath.with_suffix('.bak_hr_test')
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(original)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ day-81-rvn.md gefixt (backup gemaakt)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/test-fix-hr.py _social-posts/nl/day-81-rvn.md [--update]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    update = "--update" in sys.argv

    test_fix_hr(filepath, update)