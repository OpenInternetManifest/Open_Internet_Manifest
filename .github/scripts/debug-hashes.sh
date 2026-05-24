#!/bin/bash
# debug-hashes.sh - Gerichte debug met titel behouden

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Gebruik: ./debug-hashes.sh path/to/file.md"
  exit 1
fi

echo "=== DEBUG HASH CALCULATION ==="
echo "Bestand: $FILE"
echo "========================================"

raw_body=$(awk '
  BEGIN { in_body = 0 }
  /^---$/ {
    if (in_body == 0) { in_body = 1; next }
    else { in_body = 2; next }
  }
  in_body == 2 { print }
' "$FILE")

if [ ${#raw_body} -lt 300 ]; then
  raw_body=$(sed -n '/^---$/,/^---$/!p' "$FILE" | sed '/^---$/d')
fi

fuzzy_body=$(python3 tools/fuzzy_clean.py <<< "$raw_body")

echo -e "\n=== VOLLEDIGE FUZZY CLEANED TEXT (titel behouden) ==="
echo "$fuzzy_body"
echo "========================================"

fuzzy_sha256=$(echo -n "$fuzzy_body" | sha256sum | awk "{print \$1}")

echo "Fuzzy cleaned length: ${#fuzzy_body} karakters"
echo "fuzzy_sha256 = $fuzzy_sha256"
echo "========================================"