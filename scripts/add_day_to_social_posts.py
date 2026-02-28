# scripts/add_day_to_social_posts.py
import os
import re
import yaml
from pathlib import Path

POST_DIRS = [
    Path("nl/social-posts"),
    Path("en/social-posts"),
]

def add_day_to_file(file_path):
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

    # Haal dag-nummer uit bestandsnaam
    filename = file_path.stem
    match = re.search(r'(?:dag|day)-(\d+)(?:-rvn|-teaser)?', filename)
    if not match:
        print(f"Geen dag-nummer in filename {filename}")
        return

    day_num = int(match.group(1))

    # Voeg day toe als hij mist of leeg is
    if "day" not in fm or fm["day"] == '' or fm["day"] is None:
        fm["day"] = day_num
        print(f"Day toegevoegd aan {file_path}: {day_num}")
    elif fm["day"] != day_num:
        print(f"Waarschuwing: {file_path} heeft day: {fm['day']} maar filename impliceert {day_num}")
    else:
        print(f"Day al correct in {file_path}")

    # Schrijf terug
    new_fm = "---\n" + yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False) + "---\n"
    final_content = new_fm + content[fm_match.end():].lstrip()

    backup_path = file_path.with_suffix(file_path.suffix + ".backup-day")
    file_path.rename(backup_path)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Geüpdatet: {file_path}")

# Run
for dir_path in POST_DIRS:
    if not dir_path.exists():
        print(f"Map niet gevonden: {dir_path}")
        continue
    print(f"Verwerken map: {dir_path}")
    for file in dir_path.glob("**/*.md"):
        add_day_to_file(file)

print("Klaar! Check git diff en test pijlen.")