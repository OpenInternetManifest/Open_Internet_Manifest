#!/usr/bin/env python3
# tools/add-clean-text-from-raw.py - Bulk update clean_text using central fuzzy_clean.py

import sys
import re
from pathlib import Path

# Import the central clean function
sys.path.append(str(Path(__file__).parent))
from fuzzy_clean import fuzzy_clean

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter and body
    match = re.match(r'^(---\s*\n[\s\S]*?\n---\s*\n)([\s\S]*)$', content, re.MULTILINE)
    if not match:
        print(f"⚠️  Geen geldige frontmatter: {filepath}")
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    # Check for raw_markdown
    raw_match = re.search(r'raw_markdown:\s*\|?\s*\n((?: {2,}|\t| {4,}).*?)(?=\n\S|\n---|\Z)', frontmatter, re.DOTALL)
    if not raw_match:
        print(f"⚠️  Geen raw_markdown gevonden in: {filepath}")
        return False

    raw_markdown = raw_match.group(1).strip()

    # Use central fuzzy_clean
    clean_text = fuzzy_clean(raw_markdown)

    # Update or add clean_text in frontmatter
    if 'clean_text:' in frontmatter:
        # Replace existing clean_text
        new_front = re.sub(
            r'clean_text:[\s\S]*?(?=\n\w+:|\n---)', 
            f'clean_text: |-\n{clean_text}\n', 
            frontmatter
        )
    else:
        # Insert before closing ---
        new_front = re.sub(
            r'(\n---\s*)$', 
            f'\nclean_text: |-\n{clean_text}\n---', 
            frontmatter
        )

    new_content = new_front + body

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Updated clean_text: {filepath.name}")
    return True


# ==================== MAIN ====================
if __name__ == "__main__":
    base_dir = Path("_social-posts")
    
    for lang in ["nl", "en"]:
        dir_path = base_dir / lang
        if not dir_path.exists():
            continue
            
        print(f"\n=== Processing language: {lang} ===")
        count = 0
        for file in sorted(dir_path.glob("day-*.md")):
            if update_file(file):
                count += 1
                
        print(f"   → {count} files bijgewerkt in {lang}/")