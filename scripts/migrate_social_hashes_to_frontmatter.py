# scripts/migrate_social_hashes_to_frontmatter.py
# Migratie-script: haalt hashes uit official-hashes.js en zet ze in social_fb_sha256 / social_x_sha256

import os
import re
import yaml
import json
from pathlib import Path

HASHES_JS = Path("assets/js/official-hashes.js")

POST_DIRS = [
    Path("nl/social-posts"),
    Path("en/social-posts"),
]

def load_hashes_from_js():
    if not HASHES_JS.exists():
        print(f"JS-bestand niet gevonden: {HASHES_JS}")
        return {}

    with open(HASHES_JS, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex om het object te pakken
    match = re.search(r'officialHashes\s*=\s*({[\s\S]*?});', content, re.MULTILINE)
    if not match:
        print("Kon officialHashes niet vinden in JS.")
        print("Eerste 200 chars:")
        print(content[:200])
        return {}

    obj_str = match.group(1)
    obj_str = re.sub(r"//.*?$", "", obj_str, flags=re.MULTILINE)
    obj_str = obj_str.replace("'", '"')

    try:
        hashes = json.loads(obj_str)
        print(f"{len(hashes)} hashes geladen uit JS.")
        return hashes
    except json.JSONDecodeError as e:
        print(f"JSON parse fout: {e}")
        return {}

def migrate_file(file_path, known_hashes):
    relative_path = '/' + os.path.relpath(file_path, Path.cwd()).replace('\\', '/')
    relative_path_no_ext = relative_path.rsplit('.', 1)[0]

    # Basisnaam (dag-35-rvn of day-35-rvn)
    base_name = Path(relative_path_no_ext).name

    updated = False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verwijder oude footer als aanwezig
    content = re.sub(r"(?:Deze post is 100% authentiek|This post is 100% authentic).*", "", content, flags=re.DOTALL | re.IGNORECASE).rstrip()

    fm_match = re.match(r"---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        print(f"Geen frontmatter in {file_path}")
        return

    fm_str = fm_match.group(1)
    try:
        fm = yaml.safe_load(fm_str)
    except Exception as e:
        print(f"YAML fout in {file_path}: {e}")
        return

    # Probeer hashes te matchen voor Facebook en X varianten
    for suffix, field in [
        ('', 'social_fb_sha256'),     # dag-X-rvn → Facebook hoofdpost
        ('-x', 'social_x_sha256'),    # dag-X-rvn-x → X hoofdpost
    ]:
        js_key = relative_path_no_ext + suffix
        if js_key in known_hashes:
            target_hash = known_hashes[js_key]
            if field not in fm or fm[field] == '' or fm[field] is None:
                fm[field] = target_hash
                print(f"{field} gevuld met {target_hash} voor {file_path}")
                updated = True
            elif fm[field] != target_hash:
                print(f"Waarschuwing: {field} had {fm[field]}, maar JS heeft {target_hash} → overschreven")
                fm[field] = target_hash
                updated = True
            else:
                print(f"{field} al correct in {file_path}")

    if not updated:
        print(f"Geen wijziging nodig in {file_path}")
        return

    new_fm = "---\n" + yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False) + "---\n"
    final_content = new_fm + content[fm_match.end():].lstrip()

    backup_path = file_path.with_suffix(file_path.suffix + ".backup")
    file_path.rename(backup_path)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Geüpdatet: {file_path} (backup: {backup_path})")

# Hoofdscript
hashes = load_hashes_from_js()
if not hashes:
    print("Geen hashes geladen – script stoppen.")
    exit(1)

for dir_path in POST_DIRS:
    if not dir_path.exists():
        print(f"Map niet gevonden: {dir_path}")
        continue
    print(f"Verwerken map: {dir_path}")
    for file in dir_path.glob("**/*.md"):
        migrate_file(file, hashes)

print("Klaar! Check met 'git diff' en test een paar posts.")
print("Commit: git add . && git commit -m 'migrate social hashes from JS to correct frontmatter fields'")