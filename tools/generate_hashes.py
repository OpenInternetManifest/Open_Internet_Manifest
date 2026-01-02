import os
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup

SITE_DIR = Path("_site")

hashes = {}
clean_texts = {}  # Nieuw: sla clean text op voor fuzzy

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
    
    # Unwrap inline tags
    for tag in ['a', 'span', 'strong', 'em', 'i', 'b', 'u', 'code', 'mark', 'small', 'sup', 'sub']:
        for el in clone.find_all(tag):
            el.unwrap()
    
    # Replace <br> by space
    for br in clone.find_all('br'):
        br.replace_with(' ')
    
    # Collect h1 + p tags (cleanste methode)
    title = ''
    h1 = clone.find('h1')
    if h1:
        title = h1.get_text(strip=True)
    
    paragraphs = []
    for p in clone.find_all('p'):
        para_text = p.get_text(strip=True)
        if para_text:
            paragraphs.append(para_text)
    
    text = title
    if paragraphs:
        text += '\n\n' + '\n\n'.join(paragraphs)
    
    # DEBUG voor thesis-01
    if "nl/theses/thesis-01" in str(file_path):
        print("\n--- DEBUG CLEAN TEXT thesis-01 ---")
        print(repr(text))
        print("---")
    
    hash_obj = hashlib.sha256(text.encode('utf-8'))
    return hash_obj.hexdigest(), text  # Return hash + clean text

print("Zoeken in:", SITE_DIR.absolute())

for root, dirs, files in os.walk(SITE_DIR):
    for file in files:
        if file.endswith(".html"):
            file_path = Path(root) / file
            if "assets" in str(file_path):
                continue
            result = calculate_clean_hash(file_path)
            if result:
                hash_value, clean_text = result
                rel_path = file_path.relative_to(SITE_DIR).as_posix()
                clean_path = "/" + rel_path.rsplit(".", 1)[0].replace("/index", "")
                if clean_path.endswith("/"):
                    clean_path = clean_path[:-1]
                if clean_path == "/":
                    clean_path = "/"
                hashes[clean_path] = hash_value
                clean_texts[clean_path] = clean_text
                print(f"'{clean_path}': '{hash_value}',")

print("\n// Voor hash-verify.js")
print("const officialHashes = {")
for path, h in sorted(hashes.items()):
    print(f"  '{path}': '{h}',")
print("};")

print("\n// Voor fuzzy match in hash-verifier.js")
print("const preStoredTexts = {")
for path, text in sorted(clean_texts.items()):
    escaped_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('\n', '\\n')
    print(f"  '{path}': `{escaped_text}`,")  # Backticks voor multiline string
print("};")