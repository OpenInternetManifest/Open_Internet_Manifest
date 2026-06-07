#!/usr/bin/env python3
# tools/test-final-cleanup.py - Test versie op 1 post

import sys
import re
import hashlib
import textwrap
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from fuzzy_clean import fuzzy_clean

def final_fix_single(filepath, update=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract raw_markdown
    raw_match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\s*\w+\s*:|\n---|\Z)', content, re.DOTALL)
    raw_markdown = raw_match.group(1).strip() if raw_match else ""

    clean_text = fuzzy_clean(raw_markdown)

    # Bouw perfecte frontmatter
    new_front = "---\n"
    # Houd bestaande metadata
    for key in ['layout', 'lang', 'day', 'rvn_title', 'rvn_teaser', 'donation_link', 'donation_text', 'git_commit_hash', 'git_commit_url', 'git_commit_date']:
        m = re.search(rf'{key}\s*:\s*(.+?)(?=\n\s*\w+\s*:|\n---|\Z)', content)
        if m:
            val = m.group(1).strip().strip('"')
            if val:
                new_front += f"{key}: {val}\n" if not val.startswith('"') else f'{key}: "{val}"\n'

    new_front += f"raw_markdown: |\n{textwrap.indent(raw_markdown, '  ')}\n\n"
    new_front += f"clean_text: |-\n{textwrap.indent(clean_text, '  ')}\n\n"
    new_front += f"full_sha256: {hashlib.sha256(raw_markdown.encode()).hexdigest()}\n"
    new_front += f"fuzzy_sha256: {hashlib.sha256(clean_text.encode()).hexdigest()}\n"
    new_front += "---\n"

    # Verwijder oude frontmatter + eventuele clean_text in body
    new_content = re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n', new_front, content, flags=re.MULTILINE)

    if not update:
        print(f"\n=== TEST OP {filepath.name} ===")
        print(new_front)
        print("--- RAW (eerste 500) ---")
        print(raw_markdown[:500] + "..." if len(raw_markdown) > 500 else raw_markdown)
        print("\n--- CLEAN TEXT (eerste 500) ---")
        print(clean_text[:500] + "..." if len(clean_text) > 500 else clean_text)
        return

    # Backup + schrijven
    backup = filepath.with_suffix('.bak_finaltest')
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ TEST FIXED: {filepath.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/test-final-cleanup.py <bestand.md> [--update]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    update = "--update" in sys.argv

    final_fix_single(filepath, update)