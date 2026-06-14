#!/bin/bash
# calculate-hashes.sh - Herberekent hashes op basis van raw_markdown + clean_text

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

echo "=== Processing $FILE ==="

# Extract raw_markdown
raw_markdown=$(awk '
  BEGIN { in_raw = 0 }
  /^raw_markdown:\s*\|/ { in_raw = 1; next }
  in_raw == 1 && /^  / { print substr($0, 3); next }
  in_raw == 1 && !/^  / { in_raw = 0 }
  in_raw == 1 { print }
' "$FILE")

# Extract clean_text
clean_text=$(awk '
  BEGIN { in_clean = 0 }
  /^clean_text:\s*\|/ { in_clean = 1; next }
  in_clean == 1 && /^  / { print substr($0, 3); next }
  in_clean == 1 && !/^  / { in_clean = 0 }
  in_clean == 1 { print }
' "$FILE")

# Bereken hashes
full_sha=$(echo -n "$raw_markdown" | sha256sum | awk '{print $1}')
fuzzy_sha=$(echo -n "$clean_text" | sha256sum | awk '{print $1}')

echo "full_sha256  = $full_sha"
echo "fuzzy_sha256 = $fuzzy_sha"

# Update frontmatter
python3 - <<EOF
import re
import sys

with open("$FILE", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'full_sha256:\s*[^\n]+', f'full_sha256: {full_sha}', content)
content = re.sub(r'fuzzy_sha256:\s*[^\n]+', f'fuzzy_sha256: {fuzzy_sha}', content)

with open("$FILE", "w", encoding="utf-8") as f:
    f.write(content)
EOF

echo "✅ Hashes updated in $FILE"