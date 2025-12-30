import os
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup

# Pad naar _site folder
SITE_DIR = Path("_site")

hashes = {}

def calculate_clean_hash(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    main = soup.find('main', class_='main-content')
    if not main:
        return None
    
    clone = main.__copy__()
    
    # Verwijder exact dezelfde elementen als in JS
    for selector in ['.integrity-check', '.community-box', '.donation-section', '.site-footer', '.page-footer', '.copy-container', '#copy-feedback', '#verify-feedback']:
        for el in clone.select(selector):
            el.decompose()
    
    # Verwijder <br> tags
    for br in clone.find_all('br'):
        br.replace_with(' ')  # Vervang door space om woorden te houden zonder extra newlines
    
    # Exact browser textContent
    text = clone.get_text(separator='\n', strip=True)
    
    # Exact zoals JS
    text = text.strip()
    text = '\n\n'.join([line for line in text.split('\n') if line.strip()])
    
    hash_obj = hashlib.sha256(text.encode('utf-8'))
    return hash_obj.hexdigest()

print("Zoeken in:", SITE_DIR.absolute())

for root, dirs, files in os.walk(SITE_DIR):
    for file in files:
        if file.endswith(".html"):
            file_path = Path(root) / file
            if "assets" in str(file_path):
                continue
            hash_value = calculate_clean_hash(file_path)
            if hash_value:
                rel_path = file_path.relative_to(SITE_DIR).as_posix()
                clean_path = "/" + rel_path.rsplit(".", 1)[0].replace("/index", "")
                if clean_path.endswith("/"):
                    clean_path = clean_path[:-1]
                if clean_path == "/":
                    clean_path = "/"
                hashes[clean_path] = hash_value
                print(f"'{clean_path}': '{hash_value}',")

print("\nKopieer dit in hash-verify.js:")
print("const hashes = {")
for path, h in sorted(hashes.items()):
    print(f"  '{path}': '{h}',")
print("};")