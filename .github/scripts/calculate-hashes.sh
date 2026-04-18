#!/bin/bash
# calculate-hashes.sh - Exact match with debug tool Versie 27

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE"
  exit 1
fi

# Stap 1: Extract body after second ---
raw_body=$(sed '0,/^---$/d' "$FILE" | sed '0,/^---$/d')

# Stap 2: WEBSITE BODY - exact zoals debug Versie 27
website_body=$(echo "$raw_body" | \
  sed 's/\*\*\(.*?\)\*\*/\1/g' | \
  sed 's/\*\(.*?\)\*/\1/g' | \
  sed 's/\*\*/ /g' | \
  sed 's/\*//g' | \
  sed 's/^>[ \t]*//g' | \
  sed 's/^[ \t]*[-*+][ \t]*//g' | \
  sed 's/^[ \t]*###*[ \t]*//g' | \
  sed 's/^[ \t]*[0-9]\+\.[ \t]*//g' | \
  sed 's/^[ \t]*//g' | \
  sed 's/[ \t]*$//g' | \
  sed '/^--$/d' | \
  sed '/^---$/d' | \
  sed '/^$/N;/^\n$/D' | \
  sed '1{/^$/d}')

# Stap 3: FUZZY BODY - volledig schoon
fuzzy_body=$(echo "$website_body" | \
  tr '[:upper:]' '[:lower:]' | \
  sed '/^$/d' | \
  sed 's/[ \t]\+/ /g')

# Bereken hashes
website_sha256=$(echo -n "$website_body" | sha256sum | awk '{print $1}')
fuzzy_sha256=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

# Git info
commit_hash=$(git rev-parse HEAD)
commit_url="https://github.com/OpenInternetManifest/Open_Internet_Manifest/commit/${commit_hash}"
commit_date=$(git log -1 --format=%cI)

# Output voor de workflow
cat << EOF
WEBSITE_SHA256=${website_sha256}
FUZZY_SHA256=${fuzzy_sha256}
GIT_COMMIT_HASH=${commit_hash}
GIT_COMMIT_URL=${commit_url}
GIT_COMMIT_DATE=${commit_date}
EOF