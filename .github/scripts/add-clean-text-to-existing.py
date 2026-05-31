#!/usr/bin/env python3
"""
add-clean-text-to-existing.py - Werkende versie
"""

from pathlib import Path
import subprocess
import re

def main():
    print("🔄 Updating clean_text on all posts...\n")
    updated = 0

    for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
        for file in sorted(Path(".").glob(pattern)):
            try:
                content = file.read_text(encoding='utf-8')

                # Extract raw_markdown of body
                match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE | re.DOTALL)
                if match:
                    raw_md = match.group(1)
                else:
                    body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
                    raw_md = body_match.group(1) if body_match else content

                # Clean via centrale script
                clean = subprocess.check_output(
                    ['python3', 'tools/fuzzy_clean.py', str(file)],
                    text=True,
                    timeout=10
                ).strip()

                # Force update clean_text
                if "clean_text:" in content:
                    new_content = re.sub(r'clean_text:\s*".*?"', f'clean_text: "{clean}"', content, flags=re.DOTALL)
                else:
                    new_content = re.sub(r'(full_sha256:.*?\n)', rf'\1clean_text: "{clean}"\n', content)

                file.write_text(new_content, encoding='utf-8')
                print(f"✅ Updated {file.name}")
                updated += 1

            except Exception as e:
                print(f"❌ Error on {file.name}: {e}")

    print(f"\n🎉 Klaar! {updated} bestanden bijgewerkt.")

if __name__ == "__main__":
    main()