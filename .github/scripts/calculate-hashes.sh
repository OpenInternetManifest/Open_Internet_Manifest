#!/usr/bin/env python3
"""
calculate-hashes.py - Alleen de meegegeven post verwerken
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

    print(f"=== Processing ONLY {file.name} ===")

    content = file.read_text(encoding='utf-8')

    # Extract body
    body_match = re.search(r'^---\s*\n[\s\S]*?^---\s*\n(.*)', content, re.MULTILINE | re.DOTALL)
    raw_body = body_match.group(1) if body_match else content

    # Calculate hashes
    fuzzy_body = re.sub(r'\s+', ' ', raw_body.strip()).strip()
    fuzzy_sha256 = sha256(fuzzy_body)

    raw_match = re.search(r'raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)', content, re.MULTILINE | re.DOTALL)
    raw_md = raw_match.group(1).rstrip('\n') if raw_match else raw_body
    full_sha256 = sha256(raw_md)

    # Update frontmatter
    content = re.sub(r'fuzzy_sha256:\s*".*?"', f'fuzzy_sha256: "{fuzzy_sha256}"', content)
    content = re.sub(r'full_sha256:\s*".*?"', f'full_sha256: "{full_sha256}"', content)

    if "full_sha256:" not in content:
        content = re.sub(r'(fuzzy_sha256:.*?\n)', rf'\1full_sha256: "{full_sha256}"\n', content)

    file.write_text(content, encoding='utf-8')

    print(f"   fuzzy = {fuzzy_sha256}")
    print(f"   full  = {full_sha256}")

    # Update JS - alleen dit bestand
    try:
        import subprocess
        subprocess.run(["python3", "tools/update-clean-texts.py", str(file), fuzzy_body], check=True)
        print("   ✅ JS updated (single file)")
    except Exception as e:
        print(f"   ⚠️ JS update failed: {e}")

    print(f"✅ Done processing {file.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 calculate-hashes.py <file>")
        sys.exit(1)
    main(sys.argv[1])