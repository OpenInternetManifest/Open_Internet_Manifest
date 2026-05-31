#!/usr/bin/env python3
"""
update_clean_text_from_fuzzy.py
Gebruikt jouw eigen fuzzy_clean.py om alle clean_text velden bij te werken.
"""

import re
import sys
from pathlib import Path

# Importeer jouw bestaande fuzzy_clean functie
sys.path.append(str(Path(__file__).parent))
from fuzzy_clean import fuzzy_clean

ROOT_DIRS = [
    Path("/home/ruben/Open_Internet_Manifest/_social-posts/nl"),
    Path("/home/ruben/Open_Internet_Manifest/_social-posts/en")
]

def update_file(file_path: Path):
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Frontmatter + body scheiden
        match = re.match(r'^(---\s*\n.*?\n---\s*\n)', content, re.DOTALL | re.MULTILINE)
        if not match:
            print(f"⚠️  Geen frontmatter: {file_path.name}")
            return False

        frontmatter = match.group(1)
        body = content[match.end():]

        # Gebruik jouw fuzzy_clean op de body (of raw_markdown als aanwezig)
        cleaned = fuzzy_clean(body)

        # Verwijder bestaande clean_text
        frontmatter = re.sub(r'clean_text:.*?(?=\n\S|\n---|\Z)', '', frontmatter, flags=re.DOTALL)

        # Voeg nieuwe schone clean_text toe
        new_frontmatter = frontmatter.rstrip() + f'\nclean_text: "{cleaned}"\n'

        new_content = new_frontmatter + '---\n' + body

        file_path.write_text(new_content, encoding='utf-8')
        print(f"✅ Updated with fuzzy_clean: {file_path.name}")
        return True

    except Exception as e:
        print(f"❌ Fout bij {file_path.name}: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Updating all clean_text using fuzzy_clean.py...\n")
    
    updated = 0
    for root_dir in ROOT_DIRS:
        files = list(root_dir.rglob("*.md"))
        print(f"Processing {len(files)} files in {root_dir.name}/ ...")
        
        for f in files:
            if update_file(f):
                updated += 1
    
    print(f"\n✅ Klaar! {updated} bestanden bijgewerkt.")