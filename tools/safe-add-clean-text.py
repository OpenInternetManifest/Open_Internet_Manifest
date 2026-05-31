#!/usr/bin/env python3
# tools/safe-add-clean-text.py - Veilige bulk update van clean_text

import sys
import re
from pathlib import Path

# Import central fuzzy_clean
sys.path.append(str(Path(__file__).parent))
from fuzzy_clean import fuzzy_clean

def update_file(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^(---\s*\n)([\s\S]*?)(\n---\s*\n)([\s\S]*)$', content)
    if not match:
        print(f"⚠️  Geen geldige frontmatter: {filepath.name}")
        return False

    front_start = match.group(1)
    front_body = match.group(2)
    front_end = match.group(3)
    body = match.group(4)

    # raw_markdown ophalen
    raw_match = re.search(r'raw_markdown\s*:\s*\|?\s*\n((?:[ \t].*?\n?)*?)(?=\n\w+\s*:|\n---|\Z)', front_body, re.DOTALL)
    if not raw_match:
        print(f"⚠️  Geen raw_markdown gevonden: {filepath.name}")
        return False

    raw_markdown = raw_match.group(1).strip()
    clean_text = fuzzy_clean(raw_markdown)

    # Verwijder ALLE vorige clean_text blokken (ook als ze verkeerd staan)
    new_front_body = re.sub(r'clean_text\s*:\s*[\s\S]*?(?=\n\w+\s*:|\n---|\Z)', '', front_body, flags=re.DOTALL).strip()

    # Voeg nieuwe clean_text toe met correcte indentatie
    if new_front_body:
        new_front_body += "\n"
    new_front_body += f"clean_text: |-\n  {clean_text.replace('\n', '\n  ')}"

    new_content = front_start + new_front_body + "\n" + front_end + body

    if dry_run:
        print(f"DRY-RUN: Would update {filepath.name}")
    else:
        backup_path = filepath.with_suffix('.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated: {filepath.name}")

    return True

# ==================== MAIN ====================
if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-d" in sys.argv or "--dry" in sys.argv
    
    if dry_run:
        print("=== DRY RUN MODE - Geen bestanden worden gewijzigd ===\n")
    
    base_dir = Path("_social-posts")
    total = 0

    for lang in ["nl", "en"]:
        dir_path = base_dir / lang
        if not dir_path.exists():
            continue
        print(f"\n=== Processing {lang.upper()} ===")
        count = 0
        for file in sorted(dir_path.glob("day-*.md")):
            if update_file(file, dry_run):
                count += 1
        print(f"   → {count} bestanden verwerkt in {lang}/")
        total += count

    print(f"\nKlaar! Totaal {total} bestanden verwerkt ({'DRY RUN' if dry_run else 'echt bijgewerkt'})")