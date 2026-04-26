#!/usr/bin/env python3
import sys
import hashlib
import re
import unicodedata
from pathlib import Path
from datetime import datetime

def fuzzy_clean(text):
    if not text:
        return ""
    
    # 1. Unicode normalisatie
    text = unicodedata.normalize('NFKC', text)
    
    # 2. Emoji's verwijderen
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  
        "\U0001F300-\U0001F5FF"  
        "\U0001F680-\U0001F6FF"  
        "\U0001F1E0-\U0001F1FF"  
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    # 3. Markdown & formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'__(.*?)__', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'\*(.*?)\*', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'_(.*?)_', r'\1', text, flags=re.DOTALL)
    
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[-*+]\s+', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'^-{3,}\s*$', ' ', text, flags=re.MULTILINE)
    
    # HTML
    text = re.sub(r'<[^>]+>', '', text)
    
    # Selectieve colon cleanup
    title_colons = r'(narratief|realiteit|hoe werkt het|hoe zien we dit|de grote verbinding|de oim-boodschap|traumabinding|cognitive dissonance|identificatie|overheid en burgers|social media|relaties en sekten|politiek|dank dat je|lees zelf|check zelf|weiger mee te spelen|schokkends|en vooral)'
    text = re.sub(rf'({title_colons})\s*:\s*', r'\1 ', text, flags=re.IGNORECASE)
    
    # URLs beschermen + colons
    text = re.sub(r'https?://', '___URL___', text)
    text = re.sub(r':', ' ', text)
    text = re.sub(r'___URL___', 'https://', text)
    
    # Whitespace + lowercase
    text = re.sub(r'\s+', ' ', text)
    text = text.strip().lower()
    
    return text


def fix_file(file_path, log_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'^\s*fuzzy_sha256:.*\n?', '', content, flags=re.MULTILINE)

    match = re.search(r'^(---\s*[\s\S]*?^---\s*)', content, re.MULTILINE)
    if not match:
        print(f"⚠️  Could not find frontmatter in {file_path.name}")
        return False

    frontmatter = match.group(1)
    body = content[match.end():].lstrip()

    fuzzy_text = fuzzy_clean(body)
    fuzzy_hash = hashlib.sha256(fuzzy_text.encode('utf-8')).hexdigest()

    if f'fuzzy_sha256: "{fuzzy_hash}"' in frontmatter:
        print(f"✅ {file_path.name} already up to date")
        return True

    lines = frontmatter.strip().splitlines()
    if lines and lines[-1].strip() == '---':
        lines.pop()

    new_frontmatter = '\n'.join(lines) + f'\nfuzzy_sha256: "{fuzzy_hash}"\n---'
    new_content = new_frontmatter + '\n' + body

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Updated {file_path.name}")
    print(f"   New hash: {fuzzy_hash}")
    return True


# ==================== SINGLE FILE TEST ====================
if __name__ == "__main__":
    file_path = Path("_social-posts/nl/day-62-rvn.md")
    
    if not file_path.exists():
        print(f"❌ Bestand niet gevonden: {file_path}")
        print("Controleer het pad!")
        sys.exit(1)

    log_path = Path("fuzzy-fix-log.txt")
    
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n=== Single File Fuzzy Fix - {datetime.now()} ===\n")
        log_file.write(f"Testing: {file_path}\n")
        
        success = fix_file(file_path, log_file)
        
        if success:
            log_file.write(f"✅ Success: {file_path.name}\n")
            print("\n🎉 Klaar! day-62-rvn.md is bijgewerkt.")
        else:
            log_file.write(f"❌ Failed: {file_path.name}\n")

            # python3 fix-single-day62.py