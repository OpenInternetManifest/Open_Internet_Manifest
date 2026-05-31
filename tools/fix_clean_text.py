#!/usr/bin/env python3
import re
from pathlib import Path

ROOT_DIR = Path("/home/ruben/Open_Internet_Manifest/_social-posts/")

def safe_clean_text(text: str) -> str:
    if not text or len(text) < 5:
        return "RVN post - Open Internet Manifest"
    
    text = re.sub(r'(.{100,})\1+', r'\1', text, flags=re.DOTALL)  # herhalingen
    text = text[:350]
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'[:#"\']', ' ', text)   # maak YAML veilig
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fix_file(file_path: Path):
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Haal frontmatter eruit (robuster)
        match = re.search(r'^(---\s*\n.*?\n---\s*\n)', content, re.DOTALL | re.MULTILINE)
        if not match:
            print(f"⚠️  Geen frontmatter: {file_path.name}")
            return False

        frontmatter = match.group(1)
        body = content[match.end():]

        # Verwijder ALLE bestaande clean_text regels
        frontmatter = re.sub(r'clean_text:.*?(?=\n\S|\n---|\Z)', '', frontmatter, flags=re.DOTALL)

        # Voeg één schone clean_text toe
        clean = safe_clean_text(body[:500])   # gebruik body als backup
        new_frontmatter = frontmatter.rstrip() + f'\nclean_text: "{clean}"\n'

        new_content = new_frontmatter + '---\n' + body

        file_path.write_text(new_content, encoding='utf-8')
        print(f"✅ Geforceerd opgeschoond: {file_path.name}")
        return True

    except Exception as e:
        print(f"❌ Fout bij {file_path.name}: {e}")
        return False


# ================== RUN ==================
if __name__ == "__main__":
    print("🚀 NL v2 - Force clean_text fixer\n")
    
    files = list(ROOT_DIR.rglob("*.md"))
    print(f"{len(files)} bestanden gevonden.\n")
    
    fixed = 0
    for f in files:
        if fix_file(f):
            fixed += 1
            
    print(f"\n✅ Klaar! {fixed} bestanden verwerkt.")