#!/usr/bin/env python3
# tools/clean-frontmatter.py - v6 Line-by-line parser (betrouwbaar)
# werkende versie voor 1 post herberekenen fuzzy en full sha256, en frontmatter opschonen van overbodige velden (zoals oude hashes, of oude clean_text)
# run met python3 tools/clean-frontmatter.py _social-posts/nl/day-XX-sample.md --update

import sys
import re
import hashlib
import textwrap
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def fix_single_file(filepath, update=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Zoek begin en einde frontmatter
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if start == -1:
                start = i
            else:
                end = i
                break

    if start == -1 or end == -1:
        print("❌ Geen frontmatter")
        return

    front_lines = lines[start+1:end]
    body = ''.join(lines[end+1:])

    # Extract raw_markdown en clean_text
    raw_markdown = []
    clean_text = []
    in_raw = False
    in_clean = False

    for line in front_lines:
        stripped = line.strip()
        
        if stripped.startswith('raw_markdown:'):
            in_raw = True
            in_clean = False
            continue
        elif stripped.startswith('clean_text:'):
            in_clean = True
            in_raw = False
            continue
        elif stripped and stripped.split(':')[0].strip() in ['full_sha256', 'fuzzy_sha256', 'layout', 'lang', 'day', 'rvn_title', 'rvn_teaser', 'donation_', 'git_']:
            in_raw = False
            in_clean = False

        if in_raw:
            raw_markdown.append(line)
        elif in_clean:
            clean_text.append(line)

    raw_str = textwrap.dedent(''.join(raw_markdown)).strip()
    clean_str = textwrap.dedent(''.join(clean_text)).strip()

    full_sha = sha256(raw_str)
    fuzzy_sha = sha256(clean_str)

    # Belangrijke velden
    kept = []
    for line in front_lines:
        stripped = line.strip()
        if stripped.startswith(('layout:', 'lang:', 'day:', 'rvn_title:', 'rvn_teaser:', 'donation_', 'git_')):
            kept.append(line.rstrip())

    # Nieuwe frontmatter bouwen
    new_front = ["---\n"]
    new_front.extend([k + "\n" for k in kept])
    new_front.append(f"raw_markdown: |\n{textwrap.indent(raw_str, '  ')}\n\n")
    new_front.append(f"clean_text: |-\n{textwrap.indent(clean_str, '  ')}\n\n")
    new_front.append(f"full_sha256: {full_sha}\n")
    new_front.append(f"fuzzy_sha256: {fuzzy_sha}\n")
    new_front.append("---\n")

    new_content = ''.join(new_front) + body

    if not update:
        print(f"\n=== {filepath.name} ===")
        print(''.join(new_front))

        print("\n--- RAW MARKDOWN (eerste 6000) ---")
        print(raw_str[:6000] + ("..." if len(raw_str) > 6000 else ""))

        print("\n--- CLEAN TEXT (eerste 6000) ---")
        print(clean_str[:6000] + ("..." if len(clean_str) > 6000 else ""))

        print("\nfull_sha256  :", full_sha)
        print("fuzzy_sha256 :", fuzzy_sha)
        return

    backup = filepath.with_suffix('.bak_clean')
    backup.write_text(''.join(lines), encoding='utf-8')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ Schoon frontmatter geschreven: {filepath.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python3 tools/clean-frontmatter.py <bestand.md> [--update]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    update = "--update" in sys.argv

    fix_single_file(filepath, update)