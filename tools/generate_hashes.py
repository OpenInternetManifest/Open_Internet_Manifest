import os
import hashlib
from pathlib import Path

# Pad naar je _site folder (na jekyll build)
SITE_DIR = Path("_site")  # of "docs" als je daar bouwt

hashes = {}

def calculate_hash(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Verwijder feedback en includes (simuleer copyPageText)
    # We verwijderen alles na de laatste </main> of voor simplicity: hele content
    # Maar voor nauwkeurigheid: we gebruiken dezelfde logica als JS
    # Voor nu: hele HTML content (behalve script tags met hash-verify)
    # Simpele versie: hele content
    hash_obj = hashlib.sha256(content.encode("utf-8"))
    return hash_obj.hexdigest()

for root, dirs, files in os.walk(SITE_DIR):
    for file in files:
        if file.endswith(".html"):
            file_path = Path(root) / file
            rel_path = file_path.relative_to(SITE_DIR).as_posix()
            if rel_path.startswith("Open_Internet_Manifest/"):
                clean_path = "/" + rel_path.split("/", 1)[1].rsplit(".", 1)[0]
                clean_path = clean_path.replace("/index", "")
                if clean_path.endswith("/"):
                    clean_path = clean_path[:-1]
                if clean_path == "":
                    clean_path = "/"
                hash_value = calculate_hash(file_path)
                hashes[clean_path] = hash_value
                print(f"'{clean_path}': '{hash_value}',")

print("\nKopieer dit in hash-verify.js:")
print("const hashes = {")
for path, h in sorted(hashes.items()):
    print(f"  '{path}': '{h}',")
print("};")
