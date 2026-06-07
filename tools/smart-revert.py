#!/usr/bin/env python3
# tools/smart-revert.py - Smart revert + herstel clean_text

from pathlib import Path
import re
import textwrap

def smart_revert():
    base = Path("_social-posts")
    reverted = 0
    regenerated = 0

    for lang in ["nl", "en"]:
        for file in (base / lang).glob("day-*.md"):
            bak = file.with_suffix('.bak_clean')
            
            if bak.exists():
                # Revert naar backup
                with open(bak, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                print(f"✅ Reverted from backup: {file.name}")
                reverted += 1
            else:
                # Geen backup → probeer clean_text te regenereren
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()

                raw_match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\s*\w+\s*:|\n---|\Z)', content, re.DOTALL)
                if raw_match:
                    raw = raw_match.group(1).strip()
                    from fuzzy_clean import fuzzy_clean
                    clean = fuzzy_clean(raw)

                    # Verwijder rommel uit body
                    content = re.sub(r'clean_text:[\s\S]*?(?=\n---|\Z)', '', content, flags=re.MULTILINE)

                    # Voeg schone clean_text toe
                    new_content = re.sub(
                        r'(raw_markdown:[\s\S]*?)(?=\n\s*full_sha256:)',
                        rf'\1\nclean_text: |-\n{textwrap.indent(clean, "  ")}\n',
                        content,
                        flags=re.MULTILINE
                    )

                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"🔄 Regenerated clean_text: {file.name}")
                    regenerated += 1
                else:
                    print(f"⚠️  Probleem bij {file.name} (geen raw_markdown)")

    print(f"\nKlaar! {reverted} reverted + {regenerated} regenerated")

if __name__ == "__main__":
    smart_revert()