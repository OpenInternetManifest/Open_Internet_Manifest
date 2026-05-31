#!/usr/bin/env python3
"""
final-frontmatter-cleanup.py - Grote schoonmaak
"""

from pathlib import Path
import subprocess
import re

def main():
    print("🧹 Grote frontmatter schoonmaak...\n")
    fixed = 0

    for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
        for file in sorted(Path(".").glob(pattern)):
            content = file.read_text(encoding='utf-8')

            # Extract body
            body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
            body = body_match.group(1).strip() if body_match else content

            # Clean via fuzzy_clean
            try:
                clean_text = subprocess.check_output(
                    ['python3', 'tools/fuzzy_clean.py'],
                    input=body,
                    text=True,
                    timeout=10
                ).strip()
            except:
                clean_text = re.sub(r'\s+', ' ', body.strip()).strip().lower()

            # Extract useful fields
            lang = re.search(r'lang:\s*(\w+)', content)
            day = re.search(r'day:\s*(\d+)', content)
            title = re.search(r'rvn_title:\s*"(.*?)"', content)
            teaser = re.search(r'rvn_teaser:\s*"(.*?)"', content)
            donation = re.search(r'donation_link:\s*"(.*?)"', content)

            # Bouw nette frontmatter
            new_fm = f"""---
layout: social-posts
lang: {lang.group(1) if lang else 'nl'}
day: {day.group(1) if day else '0'}
rvn_title: "{title.group(1) if title else ''}"
rvn_teaser: "{teaser.group(1) if teaser else ''}"
donation_link: "{donation.group(1) if donation else ''}"
donation_text: ""
fuzzy_sha256: ""
full_sha256: ""
clean_text: "{clean_text}"
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
raw_markdown: |
"""
            # Add raw_markdown with correct indent
            raw_block = "\n".join("  " + line for line in body.splitlines())

            new_content = new_fm + raw_block + "\n---\n\n" + body

            file.write_text(new_content, encoding='utf-8')
            print(f"✅ Opgeruimd: {file.name}")
            fixed += 1

    print(f"\n🎉 Klaar! {fixed} bestanden volledig opgeruimd.")

if __name__ == "__main__":
    main()