#!/usr/bin/env python3
import re
import hashlib
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def clean_raw_markdown(raw_block):
    """Verwijder YAML inspringing veilig"""
    if not raw_block.strip():
        return ""
    
    lines = raw_block.split('\n')
    
    # Vind minimale inspringing alleen op niet-lege regels
    non_empty_lines = [line for line in lines if line.strip()]
    if not non_empty_lines:
        return raw_block.strip()
    
    min_indent = min((len(line) - len(line.lstrip())) for line in non_empty_lines)
    
    # Verwijder inspringing
    cleaned = '\n'.join(line[min_indent:] if len(line) >= min_indent else line for line in lines)
    return cleaned.strip()

def update_file(file_path: Path):
    print(f"\n{'='*90}")
    print(f"🔍 Processing: {file_path.name}")
    
    content = file_path.read_text(encoding='utf-8')
    original = content

    match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE)
    if not match:
        print("❌ Geen raw_markdown block gevonden!")
        return False

    raw_with_indent = match.group(1).rstrip('\n')
    clean_md = clean_raw_markdown(raw_with_indent)

    print(f"   📏 Originele block: {len(raw_with_indent)} chars")
    print(f"   📏 Schoon: {len(clean_md)} chars")

    new_hash = sha256(clean_md)
    print(f"   🔢 BEREKENDE full_sha256: {new_hash}")

    # Update
    if 'full_sha256:' in content:
        content = re.sub(r'full_sha256:\s*".*?"', f'full_sha256: "{new_hash}"', content)
    else:
        content = re.sub(r'(fuzzy_sha256:.*?\n)', rf'\1full_sha256: "{new_hash}"\n', content)

    if content != original:
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ BIJGEWERKT → {new_hash[:20]}...")
        return True
    else:
        print("✓ Geen wijziging")
        return False

def main():
    print("🚀 DEBUG FULL HASH UPDATE STARTED (fixed indent handling)\n")
    updated = 0
    total = 0

    for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
        for f in sorted(Path(".").glob(pattern)):
            total += 1
            if update_file(f):
                updated += 1

    print(f"\n🎉 Klaar! {updated}/{total} bestanden bijgewerkt.")

if __name__ == "__main__":
    main()