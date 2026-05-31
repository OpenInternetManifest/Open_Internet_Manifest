#!/usr/bin/env python3
"""
fix-clean-text-urls.py - Verwijdert pad/URL uit clean_text
"""

from pathlib import Path
import re
import subprocess

def main():
    print("🔄 Cleaning URLs from clean_text...\n")
    updated = 0

    for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
        for file in sorted(Path(".").glob(pattern)):
            content = file.read_text(encoding='utf-8')

            # Check of er nog een pad in clean_text staat
            if re.search(r'clean_text:\s*"_social-posts/', content):
                # Extract raw_markdown of body
                match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE | re.DOTALL)
                if match:
                    raw_md = match.group(1)
                else:
                    body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
                    raw_md = body_match.group(1) if body_match else content

                # Clean opnieuw
                try:
                    clean = subprocess.check_output(
                        ['python3', 'tools/fuzzy_clean.py'],
                        input=raw_md,
                        text=True,
                        timeout=10
                    ).strip()
                except:
                    clean = re.sub(r'\s+', ' ', raw_md.strip()).strip().lower()

                # Update clean_text (zonder pad)
                new_content = re.sub(r'clean_text:\s*".*?"', f'clean_text: "{clean}"', content, flags=re.DOTALL)

                file.write_text(new_content, encoding='utf-8')
                print(f"✅ Fixed URL in {file.name}")
                updated += 1

    print(f"\n🎉 Klaar! {updated} bestanden gefixt.")

if __name__ == "__main__":
    main()
