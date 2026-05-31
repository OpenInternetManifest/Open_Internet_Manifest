#!/usr/bin/env python3
import re
from pathlib import Path

ROOT_DIR = Path("/home/ruben/Open_Internet_Manifest/_social-posts/nl")

def recover_file(file_path: Path):
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Haal alles wat op frontmatter lijkt eruit
        match = re.search(r'^(---\s*\n[\s\S]*?)\n---\s*\n', content, re.MULTILINE)
        if not match:
            print(f"⚠️  Geen herkenbare frontmatter: {file_path.name}")
            return False

        frontmatter = match.group(1)
        body = content[match.end():]

        # Verwijder ALLE bestaande clean_text (ook dubbele)
        frontmatter = re.sub(r'clean_text:.*?(?=\n\S|\n---|\Z)', '', frontmatter, flags=re.DOTALL | re.IGNORECASE)

        # Maak één nette clean_text van de body
        clean = re.sub(r'\s+', ' ', body[:400].strip())
        clean = re.sub(r'[:#"\']', ' ', clean)   # YAML veilig maken
        clean = clean[:350].strip()

        # Voeg correct toe (binnen frontmatter)
        if 'clean_text:' not in frontmatter:
            new_frontmatter = frontmatter.rstrip() + f'\nclean_text: "{clean}"\n'
        else:
            new_frontmatter = frontmatter

        new_content = new_frontmatter + '---\n' + body

        file_path.write_text(new_content, encoding='utf-8')
        print(f"✅ Hersteld: {file_path.name}")
        return True

    except Exception as e:
        print(f"❌ Fout bij {file_path.name}: {e}")
        return False


if __name__ == "__main__":
    print("🚨 RECOVERY MODE - nl map\n")
    
    files = list(ROOT_DIR.rglob("*.md"))
    print(f"{len(files)} bestanden gevonden.\n")
    
    fixed = 0
    for f in files:
        if recover_file(f):
            fixed += 1
            
    print(f"\n✅ Klaar! {fixed} bestanden hersteld.")