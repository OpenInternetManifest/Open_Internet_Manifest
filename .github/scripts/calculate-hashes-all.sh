#!/usr/bin/env python3
"""
calculate-hashes.py - Finale versie voor NL + EN
"""

import re
import hashlib
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def clean_raw_markdown(raw_block):
    """Verwijder alle leading whitespace per regel"""
    if not raw_block:
        return ""
    lines = raw_block.split('\n')
    cleaned_lines = [line.lstrip() for line in lines]
    cleaned = '\n'.join(cleaned_lines)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()

def main(file_path):
    file = Path(file_path)
    if not file.exists():
        print(f"Error: {file} not found")
        return

    print(f"=== Processing {file.name} ===")

    content = file.read_text(encoding='utf-8')

    # Extract raw_markdown
    raw_match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE | re.DOTALL)
    if raw_match:
        raw_with_indent = raw_match.group(1).rstrip('\n')
        raw_md = clean_raw_markdown(raw_with_indent)
        print("   ✅ raw_markdown cleaned")
    else:
        body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
        raw_md = body_match.group(1) if body_match else content
        print("   Using body")

    print(f"   Lengte na cleaning: {len(raw_md)}")

    # Hashes
    full_sha256 = sha256(raw_md)
    fuzzy_body = re.sub(r'\s+', ' ', raw_md.strip()).strip()
    fuzzy_sha256 = sha256(fuzzy_body)

    # Update frontmatter
    content = re.sub(r'fuzzy_sha256:\s*".*?"', f'fuzzy_sha256: "{fuzzy_sha256}"', content)
    content = re.sub(r'full_sha256:\s*".*?"', f'full_sha256: "{full_sha256}"', content)

    # Git info
    commit_hash = subprocess.getoutput("git rev-parse HEAD")
    commit_url = f"https://github.com/OpenInternetManifest/Open_Internet_Manifest/commit/{commit_hash}"
    commit_date = datetime.now().isoformat()

    content = re.sub(r'git_commit_hash:\s*".*?"', f'git_commit_hash: "{commit_hash}"', content)
    content = re.sub(r'git_commit_url:\s*".*?"', f'git_commit_url: "{commit_url}"', content)
    content = re.sub(r'git_commit_date:\s*".*?"', f'git_commit_date: "{commit_date}"', content)

    file.write_text(content, encoding='utf-8')

    print(f"   full  = {full_sha256}")
    print(f"   fuzzy = {fuzzy_sha256}")

    # Update JS
    try:
        subprocess.run(["python3", "tools/update-clean-texts.py", str(file), fuzzy_body], check=True)
        print("   ✅ JS updated")
    except Exception as e:
        print(f"   ⚠️ JS update failed: {e}")

    print(f"✅ Done {file.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 calculate-hashes.py <file>")
        sys.exit(1)
    main(sys.argv[1])