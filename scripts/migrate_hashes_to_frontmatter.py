# scripts/migrate_hashes_to_frontmatter.py
# Migratie-script: haalt oude hash uit footer en zet in frontmatter
# Alleen voor social-posts in /en/social-posts en /nl/social-posts

import os
import re
import yaml
from pathlib import Path

# mappen
POST_DIRS = [
    Path("en/social-posts"),
    Path("nl/social-posts"),
]

# Regex om hash te vinden in oude footer (NL + EN)
HASH_PATTERN = r"(?:Deze post is 100% authentiek|This post is 100% authentic).*?([a-f0-9]{64})"

def migrate_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Fout bij lezen {file_path}: {e}")
        return

    # Vind hash (pakt de eerste match, maar we hebben al gedupliceerden schoongemaakt)
    match = re.search(HASH_PATTERN, content, re.DOTALL | re.IGNORECASE)
    if not match:
        print(f"Geen hash gevonden in {file_path}")
        return

    old_hash = match.group(1)
    print(f"Hash gevonden in {file_path}: {old_hash}")

    # Verwijder oude footer (alles vanaf "Deze post is..." of "This post is..." tot eind)
    new_content = re.sub(r"(?:Deze post is 100% authentiek|This post is 100% authentic).*", "", content, flags=re.DOTALL | re.IGNORECASE).rstrip()

    # Parse frontmatter
    fm_match = re.match(r"---\n(.*?)\n---\n", new_content, re.DOTALL)
    if not fm_match:
        print(f"Geen frontmatter in {file_path}")
        return

    fm_str = fm_match.group(1)
    try:
        fm = yaml.safe_load(fm_str)
    except Exception as e:
        print(f"YAML parse fout in {file_path}: {e}")
        return

    # Voeg hash toe (als hij er nog niet staat)
    if "hash" not in fm:
        fm["hash"] = old_hash
    else:
        print(f"Hash al aanwezig in {file_path}, overslaan")

    # Schrijf nieuwe frontmatter (met betere formatting)
    new_fm = "---\n" + yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False) + "---\n"
    final_content = new_fm + new_content[fm_match.end():].lstrip()

    # Backup maken (veiligheid)
    backup_path = file_path.with_suffix(file_path.suffix + ".backup")
    file_path.rename(backup_path)

    # Schrijf nieuwe file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Geüpdatet: {file_path} (backup: {backup_path})")

# Run over alle mappen
for dir_path in POST_DIRS:
    if not dir_path.exists():
        print(f"Map niet gevonden: {dir_path}")
        continue
    print(f"Verwerken map: {dir_path}")
    for file in dir_path.glob("**/*.md"):
        migrate_file(file)

print("Klaar! Check met 'git diff' en test een paar posts.")