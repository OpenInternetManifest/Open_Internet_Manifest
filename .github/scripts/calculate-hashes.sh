#!/usr/bin/env python3
"""
calculate-hashes.py - Simpel, alleen de meegegeven post, geen rommel
"""

import re
import hashlib
import sys
from pathlib import Path

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main(file_path):
    file = Path(file_path)
    if not file.exists():
        print(f"Error: {file} not found")
        return

    print(f"=== Processing {file.name} ===")

    content = file.read_text(encoding='utf-8')

    # Extract body after frontmatter
    body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
    raw_body = body_match.group(1) if body_match else content

    # 1. Add raw_markdown if missing
    if "raw_markdown:" not in content:
        print("→ Adding raw_markdown...")
        clean_body = raw_body.strip()
        indented = "\n".join("  " + line for line in clean_body.splitlines())
        
        new_content = re.sub(
            r"(^---\s*\n[\s\S]*?)(^---\s*?$)",
            rf"\1raw_markdown: |\n{indented}\n\2",
            content,
            flags=re.MULTILINE
        )
        file.write_text(new_content, encoding='utf-8')
        print("   ✅ raw_markdown added")
        content = new_content

    # 2. Calculate hashes
    fuzzy_body = re.sub(r'\s+', ' ', raw_body.strip()).strip()
    fuzzy_sha256 = sha256(fuzzy_body)

    raw_match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE | re.DOTALL)
    raw_md = raw_match.group(1).rstrip('\n') if raw_match else raw_body
    full_sha256 = sha256(raw_md)

    # 3. Update frontmatter
    content = re.sub(r'fuzzy_sha256:\s*".*?"', f'fuzzy_sha256: "{fuzzy_sha256}"', content)
    content = re.sub(r'full_sha256:\s*".*?"', f'full_sha256: "{full_sha256}"', content)

    if "full_sha256:" not in content:
        content = re.sub(r'(fuzzy_sha256:.*?\n)', rf'\1full_sha256: "{full_sha256}"\n', content)

    # Add git info if missing
    if "git_commit_hash:" not in content:
        content = re.sub(r'(full_sha256:.*?\n)', rf'\1git_commit_hash: ""\ngit_commit_url: ""\ngit_commit_date: ""\n', content)

    file.write_text(content, encoding='utf-8')

    print(f"✅ Done {file.name}")
    print(f"   fuzzy = {fuzzy_sha256}")
    print(f"   full  = {full_sha256}")

    # 4. Update JS (single file)
    try:
        subprocess.run(["python3", "tools/update-clean-texts.py", str(file), fuzzy_body], check=True)
        print("   ✅ JS updated")
    except:
        print("   ⚠️ JS update failed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 calculate-hashes.py <file>")
        sys.exit(1)
    main(sys.argv[1])