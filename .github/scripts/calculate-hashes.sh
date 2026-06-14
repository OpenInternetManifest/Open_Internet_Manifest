#!/bin/bash
# calculate-hashes.sh - Herbouwt clean_text + hashes op basis van raw_markdown

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

echo "=== Processing $FILE ==="

# 1. raw_markdown extraheren
raw_markdown=$(awk '
  BEGIN { in_raw = 0 }
  /^raw_markdown:\s*\|/ { in_raw = 1; next }
  in_raw == 1 && /^  / { print substr($0, 3) }
  in_raw == 1 && !/^  / { in_raw = 0 }
' "$FILE")

# 2. clean_text herberekenen via centraal script
clean_text=$(echo "$raw_markdown" | python3 tools/fuzzy_clean.py)

# 3. Hashes berekenen
full_sha=$(echo -n "$raw_markdown" | sha256sum | awk '{print $1}')
fuzzy_sha=$(echo -n "$clean_text" | sha256sum | awk '{print $1}')

echo "Raw length     : ${#raw_markdown}"
echo "Clean length   : ${#clean_text}"
echo "full_sha256    : ${full_sha:0:16}..."
echo "fuzzy_sha256   : ${fuzzy_sha:0:16}..."

# 4. Frontmatter updaten
python3 - <<EOF
import re
import sys

with open("$FILE", "r", encoding="utf-8") as f:
    content = f.read()

# Vervang clean_text, full_sha256 en fuzzy_sha256
content = re.sub(r'clean_text\s*:\s*[\s\S]*?(?=\n\w+\s*:|\n---|\Z)', 
                 f"""clean_text: |-
  {re.sub(r'\n', '\n  ', "$clean_text")}""", 
                 content, flags=re.DOTALL)

content = re.sub(r'full_sha256\s*:\s*[^\n\r]+', f'full_sha256: {full_sha}', content)
content = re.sub(r'fuzzy_sha256\s*:\s*[^\n\r]+', f'fuzzy_sha256: {fuzzy_sha}', content)

with open("$FILE", "w", encoding="utf-8") as f:
    f.write(content)
EOF

echo "✅ clean_text + hashes bijgewerkt in $FILE"