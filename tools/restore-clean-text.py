#!/usr/bin/env python3
# tools/restore-clean-text.py - Robuuste herstel versie 2

import re
import textwrap
from pathlib import Path

def restore():
    bak_files = list(Path("_social-posts").rglob("*.bak_clean"))
    print(f"Gevonden {len(bak_files)} backup bestanden\n")

    restored = 0
    for bak in bak_files:
        orig = bak.with_suffix('')   # verwijder .bak_clean
        
        if not orig.exists():
            continue

        with open(bak, 'r', encoding='utf-8') as f:
            bak_content = f.read()

        # Zoek clean_text block - zo breed mogelijk
        match = re.search(r'clean_text\s*:\s*\|-?\s*\n((?:.*?(?:\n|$))*?)(?=\n\s*\w+\s*:|\n---|\Z)', 
                         bak_content, re.DOTALL | re.MULTILINE)

        if match:
            clean_text = textwrap.dedent(match.group(1)).strip()
        else:
            # Fallback: zoek alles na clean_text: tot de volgende key
            match = re.search(r'clean_text\s*:\s*\|?-?\s*([\s\S]*?)(?=\n\s*\w+\s*:|\n---|\Z)', bak_content)
            clean_text = match.group(1).strip() if match else ""

        if len(clean_text) > 200:   # redelijke lengte
            # Lees huidig bestand
            with open(orig, 'r', encoding='utf-8') as f:
                current = f.read()

            # Verwijder kapotte clean_text
            current = re.sub(r'clean_text\s*:\s*[\s\S]*?(?=\n\s*(?:full_sha256|fuzzy_sha256|donation_|git_))', '', current, flags=re.MULTILINE)

            # Voeg goede clean_text toe na raw_markdown
            new_content = re.sub(
                r'(raw_markdown:[\s\S]*?)(?=\n\s*full_sha256:)',
                rf'\1\nclean_text: |-\n{textwrap.indent(clean_text, "  ")}\n',
                current,
                flags=re.MULTILINE
            )

            with open(orig, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ Hersteld: {orig.name} ({len(clean_text)} chars)")
            restored += 1
        else:
            print(f"⚠️  Te korte of geen clean_text in: {bak.name}")

    print(f"\nKlaar! {restored} bestanden hersteld.")

if __name__ == "__main__":
    restore()