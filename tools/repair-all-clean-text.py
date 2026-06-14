#!/usr/bin/env python3
# tools/repair-all-clean-text.py - Herbouwt ALLE clean_text via centraal fuzzy_clean.py

import sys
import re
import subprocess
from pathlib import Path

def get_fuzzy_clean(raw_text):
    """Roep het centrale fuzzy_clean script aan"""
    try:
        result = subprocess.run(
            ['python3', 'tools/fuzzy_clean.py'],
            input=raw_text,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"   Error fuzzy_clean: {e}")
        return ""

def repair_file(filepath):
    filepath = Path(filepath)
    content = filepath.read_text(encoding='utf-8')

    # raw_markdown ophalen
    match = re.search(r'raw_markdown\s*:\s*\|-?\s*\n([\s\S]*?)(?=\n\w+\s*:|\n---\s*$|\Z)', content, re.DOTALL)
    if not match:
        print(f"⚠️  Geen raw_markdown: {filepath.name}")
        return False

    raw = match.group(1)
    clean = get_fuzzy_clean(raw)

    if not clean:
        print(f"❌ Clean mislukt: {filepath.name}")
        return False

    # Veilige multi-line block
    new_block = "clean_text: |-\n" + "\n".join("  " + line for line in clean.splitlines() if line.strip())

    # Oude clean_text verwijderen
    content = re.sub(r'clean_text\s*:\s*[\s\S]*?(?=\n\w+\s*:|\n---|\Z)', '', content, flags=re.DOTALL)

    # Nieuwe clean_text toevoegen na raw_markdown
    content = re.sub(
        r'(raw_markdown\s*:\s*\|-?\s*\n[\s\S]*?)(?=\n\w+\s*:|\n---|\Z)',
        r'\1\n' + new_block,
        content,
        flags=re.DOTALL
    )

    filepath.write_text(content, encoding='utf-8')
    print(f"✅ Hersteld via fuzzy_clean: {filepath.name}")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single file
        repair_file(sys.argv[1])
    else:
        # Alles
        print("🔄 Herbouwen van ALLE clean_text via centraal fuzzy_clean.py...\n")
        count = 0
        for pattern in ["_social-posts/nl/*.md", "_social-posts/en/*.md"]:
            for file in sorted(Path(".").glob(pattern)):
                if repair_file(file):
                    count += 1
        print(f"\n🎉 Klaar! {count} bestanden bijgewerkt.")