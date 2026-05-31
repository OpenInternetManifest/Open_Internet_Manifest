#!/usr/bin/env python3
import re
from pathlib import Path

def repair_file(file_path):
    content = file_path.read_text(encoding='utf-8')
    original = content

    # Extract the real body (alles na de eerste frontmatter)
    body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
    if not body_match:
        print(f"⚠️ Geen body gevonden: {file_path.name}")
        return False

    body = body_match.group(1).strip()

    # Maak een schone frontmatter
    clean_fm = """---
layout: social-posts
lang: {lang}
day: {day}
rvn_title: "{title}"
rvn_teaser: "{teaser}"
donation_link: ""
donation_text: ""
fuzzy_sha256: ""
full_sha256: ""
clean_text: ""
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
raw_markdown: |
""".format(
        lang=re.search(r'lang:\s*(\w+)', content).group(1) if re.search(r'lang:\s*(\w+)', content) else 'en',
        day=re.search(r'day:\s*(\d+)', content).group(1) if re.search(r'day:\s*(\d+)', content) else '0',
        title=re.search(r'rvn_title:\s*"(.*?)"', content).group(1) if re.search(r'rvn_title:\s*"(.*?)"', content) else '',
        teaser=re.search(r'rvn_teaser:\s*"(.*?)"', content).group(1) if re.search(r'rvn_teaser:\s*"(.*?)"', content) else ''
    )

    # Voeg raw_markdown toe
    raw_block = "\n".join("  " + line for line in body.splitlines())

    new_content = clean_fm + raw_block + "\n---\n\n" + body

    if new_content != original:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"✅ Volledig gerepareerd: {file_path.name}")
        return True
    return False

print("🔨 Repareren van alle corrupt frontmatters...")

fixed = 0
for pattern in ["_social-posts/nl/day-*.md", "_social-posts/en/day-*.md"]:
    for f in sorted(Path(".").glob(pattern)):
        if repair_file(f):
            fixed += 1

print(f"\n🎉 Klaar! {fixed} bestanden volledig gerepareerd.")
print("\nRun nu:")
print("bundle exec jekyll build")
