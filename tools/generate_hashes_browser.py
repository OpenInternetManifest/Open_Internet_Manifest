import os
import hashlib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Local URL for your site (run jekyll serve first)
LOCAL_URL = "http://127.0.0.1:4000/Open_Internet_Manifest"

options = Options()
options.add_argument("--headless")  # Run without browser window
options.add_argument("--no-sandbox")  # Nodig in WSL
options.add_argument("--disable-dev-shm-usage")  # Nodig in WSL

service = Service(executable_path="/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

hashes = {}

print("Zoeken in _site en hash via browser...")

for root, dirs, files in os.walk(Path("_site")):
    for file in files:
        if file.endswith(".html"):
            file_path = Path(root) / file
            if "assets" in str(file_path):
                continue
            rel_path = file_path.relative_to(Path("_site")).as_posix()
            clean_path = "/" + rel_path.rsplit(".", 1)[0].replace("/index", "")
            if clean_path.endswith("/"):
                clean_path = clean_path[:-1]
            if clean_path == "/":
                clean_path = "/"
            url = LOCAL_URL + clean_path
            driver.get(url)
            try:
                main = driver.find_element(By.CSS_SELECTOR, '.main-content')
                text = main.text
                text = text.strip()
                # Exact zoals JS: replace 3+ newlines met \n\n
                while '\n\n\n' in text:
                    text = text.replace('\n\n\n', '\n\n')
                hash_obj = hashlib.sha256(text.encode('utf-8'))
                hash_value = hash_obj.hexdigest()
                hashes[clean_path] = hash_value
                print(f"'{clean_path}': '{hash_value}',")
            except Exception as e:
                print(f"Skip {clean_path} – no main-content or error: {e}")

driver.quit()

print("\nKopieer dit in hash-verify.js:")
print("const hashes = {")
for path, h in sorted(hashes.items()):
    print(f"  '{path}': '{h}',")
print("};")