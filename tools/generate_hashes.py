import os
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup

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
    
    # Verwijder excludes
    for selector in ['.integrity-check', '.community-box', '.donation-section', '.site-footer', '.footer-nav', '.site-footer-credits', '.page-footer', '.copy-container', '#copy-feedback', '#verify-feedback']:
        for el in clone.select(selector):
            el.decompose()
    
    # Collect title from h1
    title = ''
    h1 = clone.find('h1')
    if h1:
        # Unwrap inline in h1
        for tag in ['a', 'span', 'strong', 'em', 'i', 'b', 'u', 'code', 'mark', 'small', 'sup', 'sub']:
            for el in h1.find_all(tag):
                el.unwrap()
        # Replace <br> by space
        for br in h1.find_all('br'):
            br.replace_with(' ')
        # Get text with separator ' ' to join inline with space
        title = h1.get_text(separator=' ', strip=True)
        title = ' '.join(title.split())  # reduce multiple spaces

    # Collect paragraphs from p tags
    paragraphs = []
    for p in clone.find_all('p'):
        # Unwrap inline in p
        for tag in ['a', 'span', 'strong', 'em', 'i', 'b', 'u', 'code', 'mark', 'small', 'sup', 'sub']:
            for el in p.find_all(tag):
                el.unwrap()
        # Replace <br> by space
        for br in p.find_all('br'):
            br.replace_with(' ')
        # Get text with separator ' ' to join inline with space
        para_text = p.get_text(separator=' ', strip=True)
        para_text = ' '.join(para_text.split())  # reduce multiple spaces
        if para_text:
            paragraphs.append(para_text)
    
    # Join title + paragraphs with \n\n
    text = title
    if paragraphs:
        text += '\n\n' + '\n\n'.join(paragraphs)
    
    # DEBUG for /nl/theses/thesis-01
    if "nl/theses/thesis-01" in str(file_path):
        print("\n--- DEBUG: CLEAN TEXT VOOR /nl/theses/thesis-01 ---")
        print(repr(text))
        print("--- EINDE DEBUG ---")
        print("DEBUG HASH:", hashlib.sha256(text.encode('utf-8')).hexdigest())
        print("---\n")
    
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