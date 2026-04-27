#!/usr/bin/env python3
"""
generate-clean-texts.py
Genereert een JavaScript object met alle fuzzy clean teksten voor de verifier.
"""

import re
import unicodedata
from pathlib import Path

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
    
    # Markdown & formatting
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
    
    text = re.sub(r'<[^>]+>', '', text)
    
    title_colons = r'(narratief|realiteit|hoe werkt het|hoe zien we dit|de grote verbinding|de oim-boodschap|traumabinding|cognitive dissonance|identificatie|overheid en burgers|social media|relaties en sekten|politiek|dank dat je|lees zelf|check zelf|weiger mee te spelen|schokkends|en vooral|passiviteit)'
    text = re.sub(rf'({title_colons})\s*:\s*', r'\1 ', text, flags=re.IGNORECASE)
    
    text = re.sub(r'https?://', '___URL___', text)
    text = re.sub(r':', ' ', text)
    text = re.sub(r'___URL___', 'https://', text)
    
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text


def main():
    base_dir = Path(".")
    patterns = ["_social-posts/nl/day-*-rvn.md", "_social-posts/en/day-*-rvn.md"]

    print("Generating clean texts for verifier...\n")

    js_output = "window.officialCleanTexts = {\n"

    for pattern in patterns:
        for file_path in sorted(base_dir.glob(pattern)):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract body
            match = re.search(r'^(---\s*[\s\S]*?^---\s*)', content, re.MULTILINE)
            if not match:
                continue
            body = content[match.end():].lstrip()

            clean_text = fuzzy_clean(body)
            web_path = str(file_path).replace('\\', '/').replace('._social-posts', '/social-posts')

            # Escape voor JavaScript
            escaped = clean_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            
            js_output += f'  "{web_path}": "{escaped}",\n'
            print(f"✓ {file_path.name}")

    js_output = js_output.rstrip(',\n') + "\n};\n"
    
    output_file = Path("static/js/official-clean-texts.js")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(js_output, encoding='utf-8')

    print(f"\n🎉 Klaar! {output_file} gegenereerd.")
    print("Laad dit bestand in je verifier pagina vóór hash-verifier.js")

if __name__ == "__main__":
    main()

    # run with: python3 tools/generate-clean-texts.py