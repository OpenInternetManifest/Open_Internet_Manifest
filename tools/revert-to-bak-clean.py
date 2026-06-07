#!/usr/bin/env python3
# tools/revert-to-first-bak.py - Correcte revert naar oudste .bak_hr_*

from pathlib import Path

def revert_to_first_bak():
    base = Path("_social-posts")
    reverted = 0
    missing = 0

    for lang in ["nl", "en"]:
        for md_file in (base / lang).glob("day-*.md"):
            # Zoek alle backups voor dit bestand
            pattern = f"{md_file.name}.bak_hr_*"
            bak_files = list((base / lang).glob(pattern))
            
            if bak_files:
                # Neem de oudste backup (kleinste timestamp)
                bak_files.sort(key=lambda x: x.name)
                best_bak = bak_files[0]
                
                with open(best_bak, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                
                print(f"✅ Reverted: {md_file.name} ← {best_bak.name}")
                reverted += 1
            else:
                missing += 1
                print(f"⚠️  Geen backup voor: {md_file.name}")

    print(f"\nKlaar! {reverted} bestanden teruggezet.")
    print(f"{missing} bestanden hadden geen backup.")

if __name__ == "__main__":
    revert_to_first_bak()