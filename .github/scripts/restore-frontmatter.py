#!/usr/bin/env python3
"""
restore-frontmatter.py - Betere titel & teaser extractie
"""

from pathlib import Path
import re

def extract_title(body):
    # Meest voorkomende patronen
    patterns = [
        r'^\s*\*?\*?RVN:?\s*“?(.*?)”?\*?\*?',   # **RVN: “Titel”**
        r'RVN:\s*“?(.*?)”?',                     # RVN: “Titel”
        r'^#\s*(.*)',                            # # Titel
        r'^(.*?)[\n—-]',                         # Eerste regel
    ]
    for pat in patterns:
        m = re.search(pat, body, re.MULTILINE | re.IGNORECASE)
        if m and m.group(1).strip():
            return m.group(1).strip()[:150]
    return "Untitled"

def extract_teaser(body):
    patterns = [
        r'(Narratief|Narrative)[:\s]*(.*)', 
        r'(Realiteit|Reality)[:\s]*(.*)',
        r'(Teaser|Summary)[:\s]*(.*)',
    ]
    for pat in patterns:
        m = re.search(pat, body, re.MULTILINE | re.IGNORECASE)
        if m and m.group(2).strip():
            return m.group(2).strip()[:200]
    return "No teaser available"

def main():
    print("🔄 Herstellen van titels en teasers...\n")
    fixed = 0

    for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
        for file in sorted(Path(".").glob(pattern)):
            content = file.read_text(encoding='utf-8')
            original = content

            # Extract body
            body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
            body = body_match.group(1) if body_match else content

            title = extract_title(body)
            teaser = extract_teaser(body)

            # Update title & teaser
            content = re.sub(r'rvn_title:\s*".*?"', f'rvn_title: "{title}"', content)
            content = re.sub(r'rvn_teaser:\s*".*?"', f'rvn_teaser: "{teaser}"', content)

            if content != original:
                file.write_text(content, encoding='utf-8')
                print(f"✅ Hersteld titel/teaser: {file.name}")
                fixed += 1
            else:
                print(f"✓ OK: {file.name}")

    print(f"\n🎉 Klaar! {fixed} bestanden bijgewerkt.")

if __name__ == "__main__":
    main()