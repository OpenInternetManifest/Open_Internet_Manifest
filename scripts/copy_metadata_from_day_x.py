# scripts/copy_metadata_from_day_x.py
# Kopieert rvn_title/url/teaser en teaser_title/url/text uit dag-X.md naar rvn- en teaser-files

import os
import re
import yaml
from pathlib import Path

POST_DIRS = [
    Path("nl/social-posts"),
    Path("en/social-posts"),
]

def get_day_from_filename(filename):
    match = re.search(r'(?:dag|day)-(\d+)(?:-rvn|-teaser)?', filename)
    if match:
        return int(match.group(1))
    return None

def get_overview_file(day_num, lang_dir):
    overview_name = f"dag-{day_num}.md" if 'nl' in str(lang_dir) else f"day-{day_num}.md"
    path = lang_dir / overview_name
    if path.exists():
        return path
    print(f"Geen overzichtsfile voor dag {day_num} in {lang_dir}")
    return None

def copy_metadata(file_path, overview_path, is_rvn):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r"---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        print(f"Geen frontmatter in {file_path}")
        return

    fm_str = fm_match.group(1)
    try:
        fm = yaml.safe_load(fm_str)
    except:
        print(f"YAML fout in {file_path}")
        return

    with open(overview_path, 'r', encoding='utf-8') as f:
        overview_content = f.read()

    overview_fm_match = re.match(r"---\n(.*?)\n---\n", overview_content, re.DOTALL)
    if overview_fm_match:
        overview_fm = yaml.safe_load(overview_fm_match.group(1))
    else:
        overview_fm = {}

    updated = False

    if is_rvn:
        for field in ["rvn_title", "rvn_url", "rvn_teaser"]:
            if field not in fm or fm[field] == '':
                if field in overview_fm:
                    fm[field] = overview_fm[field]
                    print(f"{field} toegevoegd aan {file_path}")
                    updated = True
    else:
        for field in ["teaser_title", "teaser_url", "teaser_text"]:
            if field not in fm or fm[field] == '':
                if field in overview_fm:
                    fm[field] = overview_fm[field]
                    print(f"{field} toegevoegd aan {file_path}")
                    updated = True

    if not updated:
        print(f"Geen wijziging nodig in {file_path}")
        return

    new_fm = "---\n" + yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False) + "---\n"
    final_content = new_fm + content[fm_match.end():].lstrip()

    backup_path = file_path.with_suffix(file_path.suffix + ".backup-copy")
    file_path.rename(backup_path)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Geüpdatet: {file_path} (backup: {backup_path})")

# Hoofdscript
for dir_path in POST_DIRS:
    if not dir_path.exists():
        print(f"Map niet gevonden: {dir_path}")
        continue
    print(f"Verwerken map: {dir_path}")
    
    for file in dir_path.glob("**/*.md"):
        filename = file.stem
        day_num = get_day_from_filename(filename)
        if not day_num:
            print(f"Geen dag-nummer in {filename} – skip")
            continue

        overview_file = get_overview_file(day_num, dir_path)
        if not overview_file:
            continue

        is_rvn = '-rvn' in filename
        copy_metadata(file, overview_file, is_rvn)

print("Klaar! Check git diff en test grid/pijlen.")
print("Commit: git add . && git commit -m 'copy rvn/teaser metadata from dag-X.md'")