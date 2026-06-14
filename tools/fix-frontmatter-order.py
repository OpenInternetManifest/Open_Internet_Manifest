#!/usr/bin/env python3
# tools/fix-frontmatter-order.py - Veilige frontmatter order fixer met goede preview

import sys
import re
import shutil
from pathlib import Path

def needs_reordering(front_body):
    """Check of raw_markdown en clean_text in de juiste volgorde staan"""
    raw_pos = front_body.find("raw_markdown:")
    clean_pos = front_body.find("clean_text:")
    return raw_pos == -1 or clean_pos == -1 or raw_pos > clean_pos

def fix_order(filepath, update=False):
    filepath = Path(filepath)
    content = filepath.read_text(encoding='utf-8')

    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content, re.DOTALL)
    if not match:
        print(f"❌ Ongeldige frontmatter: {filepath.name}")
        return False

    front_body = match.group(2)

    if not needs_reordering(front_body):
        if not update:
            print(f"✓ Al goed: {filepath.name}")
        return False

    # Backup alleen bij echte update
    if update:
        backup = filepath.with_suffix('.bak_order')
        shutil.copy2(filepath, backup)

    # Extract blocks
    raw_match = re.search(r'(raw_markdown\s*:\s*\|-?\s*\n[\s\S]*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)
    clean_match = re.search(r'(clean_text\s*:\s*\|-?\s*\n[\s\S]*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)

    raw_block = raw_match.group(1).strip() if raw_match else ""
    clean_block = clean_match.group(1).strip() if clean_match else ""

    # Overige velden (behalve raw en clean)
    other = re.sub(r'(raw_markdown|clean_text)\s*:\s*[\s\S]*?(?=\n\w+\s*:|\n---|\Z)', '', front_body, flags=re.DOTALL).strip()

    # Nieuwe frontmatter bouwen
    new_front = "---\n"
    if other:
        new_front += other + "\n\n"
    if raw_block:
        new_front += raw_block + "\n\n"
    if clean_block:
        new_front += clean_block + "\n\n"

    # Hashes onderaan
    for line in front_body.split('\n'):
        stripped = line.strip()
        if stripped.startswith(('full_sha256:', 'fuzzy_sha256:')):
            new_front += stripped + "\n"

    new_front = new_front.strip() + "\n---\n"
    new_content = new_front + match.group(4)

    if not update:
        print(f"Would reorder → {filepath.name}")
        return True
    else:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"✅ Order gefixt: {filepath.name}")
        return True


if __name__ == "__main__":
    update = "--update" in sys.argv

    print("🔄 Frontmatter Order Fixer (dry-run)\n")

    total = 0
    to_fix = 0

    for lang in ["nl", "en"]:
        for file in sorted(Path(f"_social-posts/{lang}").glob("*.md")):
            total += 1
            if fix_order(file, update):
                to_fix += 1

    print(f"\n=== SAMENVATTING ===")
    print(f"Totaal bestanden bekeken : {total}")
    print(f"Bestanden die aangepast zouden worden : {to_fix}")
    if not update:
        print("\nGebruik --update om echt toe te passen.")
    else:
        print(f"\n🎉 {to_fix} bestanden bijgewerkt.")