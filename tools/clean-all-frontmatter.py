#!/usr/bin/env python3
# tools/clean-all-frontmatter.py - Bulk cleanup met SHA preview

import sys
from pathlib import Path
import subprocess

def get_sha_preview(filepath):
    try:
        result = subprocess.run(
            ["python3", "tools/clean-frontmatter.py", str(filepath)],
            capture_output=True, text=True
        )
        full = "unknown"
        fuzzy = "unknown"
        
        for line in result.stdout.splitlines():
            if "full_sha256  :" in line:
                full = line.split(":")[-1].strip()[:5]
            if "fuzzy_sha256 :" in line:
                fuzzy = line.split(":")[-1].strip()[:5]
        
        return full, fuzzy
    except:
        return "err", "err"

def process_file(filepath, dry_run=True):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'raw_markdown:' not in content or 'clean_text:' not in content:
            print(f"⚠️  Mist raw of clean: {filepath.name}")
            return False

        full_preview, fuzzy_preview = get_sha_preview(filepath)

        if dry_run:
            print(f"DRY-RUN: Would clean {filepath.name} | full: {full_preview} | fuzzy: {fuzzy_preview}")
            return True
        else:
            result = subprocess.run(
                ["python3", "tools/clean-frontmatter.py", str(filepath), "--update"],
                capture_output=True, text=True
            )
            if "✅ Schoon frontmatter" in result.stdout:
                print(f"✅ Opgeruimd: {filepath.name} | full: {full_preview} | fuzzy: {fuzzy_preview}")
                return True
            else:
                print(f"❌ Probleem bij {filepath.name}")
                return False

    except Exception as e:
        print(f"Error bij {filepath.name}: {e}")
        return False

if __name__ == "__main__":
    base = Path("_social-posts")
    dry_run = "--update" not in sys.argv

    if dry_run:
        print("🚀 DRY RUN - Geen bestanden worden gewijzigd\n")
    else:
        print("🔥 LIVE UPDATE - Bestanden worden gewijzigd\n")

    nl_files = list(base.glob("nl/*.md"))
    en_files = list(base.glob("en/*.md"))
    all_files = nl_files + en_files

    print(f"Totaal bestanden: {len(all_files)} ({len(nl_files)} nl + {len(en_files)} en)\n")

    success = 0
    for file in all_files:
        if process_file(file, dry_run):
            success += 1

    print(f"\nKlaar! {success}/{len(all_files)} bestanden verwerkt")
    if dry_run:
        print("\nAls alles goed lijkt, run dan:")
        print("python3 tools/clean-all-frontmatter.py --update")