#!/bin/bash
# calculate-hashes.sh - Fuzzy hash (consistent met Nexus Quick Post + verifier)

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

echo "=== Processing: $FILE ===" >&2

# ==================== BODY EXTRACTION ====================
raw_body=$(awk '
  BEGIN { in_body = 0 }
  /^---$/ {
    if (in_body == 0) { in_body = 1; next }
    else { in_body = 2; next }
  }
  in_body == 2 { print }
' "$FILE")

# Fallback als awk niet goed werkt
if [ ${#raw_body} -lt 300 ]; then
  raw_body=$(sed -n '/^---$/,/^---$/!p' "$FILE" | sed '/^---$/d')
fi

# ==================== FUZZY CLEAN ====================
fuzzy_body=$(python3 tools/fuzzy_clean.py <<< "$raw_body")

fuzzy_sha256=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

# Full hash van raw body (ter info, niet meer primair gebruikt)
full_sha256=$(echo -n "$raw_body" | sha256sum | awk '{print $1}')

# ==================== UPDATE official-clean-texts.js ====================
python3 tools/update-clean-texts.py "$FILE" "$fuzzy_body"

# ==================== DEBUG OUTPUT ====================
echo "=== DEBUG: Raw body length   = ${#raw_body} ===" >&2
echo "=== DEBUG: Fuzzy body length = ${#fuzzy_body} ===" >&2
echo "=== DEBUG: fuzzy_sha256      = $fuzzy_sha256 ===" >&2

commit_hash=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
commit_url="https://github.com/OpenInternetManifest/Open_Internet_Manifest/commit/${commit_hash}"
commit_date=$(git log -1 --format=%cI 2>/dev/null || echo "unknown")

cat << EOF
fuzzy_sha256=${fuzzy_sha256}
full_sha256=${full_sha256}
GIT_COMMIT_HASH=${commit_hash}
GIT_COMMIT_URL=${commit_url}
GIT_COMMIT_DATE=${commit_date}
EOF