#!/usr/bin/env python3
import sys
import hashlib
import re
import unicodedata

if len(sys.argv) < 2:
    print("Usage: python3 show-fuzzy-text-complete-debug.py path/to/day-XX-rvn.md")
    sys.exit(1)

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove old fuzzy_sha256
content = re.sub(r'^\s*fuzzy_sha256:.*\n?', '', content, flags=re.MULTILINE)

# Extract frontmatter and body
match = re.search(r'^(---\s*[\s\S]*?^---\s*)', content, re.MULTILINE)
if not match:
    print("Could not find frontmatter")
    sys.exit(1)

frontmatter = match.group(1)
body = content[match.end():].lstrip()

def fuzzy_clean(text):
    if not text:
        return ""
    
    text = unicodedata.normalize('NFKC', text)
    
    # Emoji's verwijderen
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
    
    # Markdown stripping
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
    
    # Titel-colons selectief verwijderen (geen URLs breken)
    title_colons = r'(narratief|realiteit|hoe werkt het|hoe zien we dit|de grote verbinding|de oim-boodschap|traumabinding|cognitive dissonance|identificatie|overheid en burgers|social media|relaties en sekten|politiek|dank dat je|lees zelf|check zelf|weiger mee te spelen|schokkends|en vooral)'
    text = re.sub(rf'({title_colons})\s*:\s*', r'\1 ', text, flags=re.IGNORECASE)
    
    # Alle overgebleven colons naar spatie (behalve in URLs)
    text = re.sub(r'https?://', '___URL___', text)   # bescherm URLs
    text = re.sub(r':', ' ', text)                   # rest colons weg
    text = re.sub(r'___URL___', 'https://', text)    # URLs herstellen (zonder extra spatie)
    
    # Whitespace normalisatie
    text = re.sub(r'\s+', ' ', text)
    text = text.strip().lower()
    
    return text

fuzzy_text = fuzzy_clean(body)
fuzzy_hash = hashlib.sha256(fuzzy_text.encode('utf-8')).hexdigest()

print("=== CALCULATED FUZZY HASH ===")
print(fuzzy_hash)
print("\n=== FULL CLEANED TEXT (emoji's verwijderd) ===")
print(fuzzy_text)
print("\n=== LENGTH ===")
print(len(fuzzy_text))

# Update file
lines = frontmatter.strip().splitlines()
if lines and lines[-1].strip() == '---':
    lines.pop()

new_frontmatter = '\n'.join(lines) + f'\nfuzzy_sha256: "{fuzzy_hash}"\n---'
new_content = new_frontmatter + '\n' + body

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n✅ File updated with new fuzzy_sha256")