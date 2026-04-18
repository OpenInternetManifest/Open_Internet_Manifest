#!/bin/bash
# calculate-hashes.sh - Fuzzy only (exact match debug v41 + tabel-bescherming)

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE"
  exit 1
fi

# Extract body after frontmatter
raw_body=$(sed '0,/^---$/d' "$FILE" | sed '0,/^---$/d')

# FUZZY BODY - zeer fuzzy, maar behoud tabellen beter
fuzzy_body=$(echo "$raw_body" | \
  sed 's/\*\*\(.*?\)\*\*/\1/g' | \
  sed 's/\*\(.*?\)\*/\1/g' | \
  sed 's/\*\*//g' | \
  sed 's/\*//g' | \
  sed 's/^>[ \t]*/ /g' | \
  sed 's/^[ \t]*###*[ \t]*/ /g' | \
  sed 's/^[ \t]*[0-9]+\.[ \t]*/ /g' | \
  sed 's/^[ \t]*[-*+][ \t]*/ /g' | \
  sed 's/^[ \t]*//g' | \
  sed 's/[ \t]*$//g' | \
  sed '/^--$/d' | \
  sed '/^---$/d' | \
  tr '[:upper:]' '[:lower:]' | \
  sed 's/[ \t]\+/ /g' | \
  tr '\n' ' ' | \
  sed 's/[ \t]\+/ /g' | \
  sed 's/^ //;s/ $//')

fuzzy_sha256=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

# Git info
commit_hash=$(git rev-parse HEAD)
commit_url="https://github.com/OpenInternetManifest/Open_Internet_Manifest/commit/${commit_hash}"
commit_date=$(git log -1 --format=%cI)

# Output
cat << EOF
fuzzy_sha256=${fuzzy_sha256}
GIT_COMMIT_HASH=${commit_hash}
GIT_COMMIT_URL=${commit_url}
GIT_COMMIT_DATE=${commit_date}
EOF