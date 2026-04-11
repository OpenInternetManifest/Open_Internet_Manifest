#!/bin/bash
# calculate-hashes.sh - Exact dezelfde hashing als debug-live-hashes.sh

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE"
  exit 1
fi

# Extract pure body after the second ---
body=$(sed '0,/^[ \t]*---[ \t]*$/d' "$FILE" | sed '0,/^[ \t]*---[ \t]*$/d')

# Clean body exactly like final debug STAP 3
clean_body=$(echo "$body" | 
  sed 's/^>[ \t]*//g' |                    # remove > from blockquotes
  sed 's/^[ \t]*[-*+][ \t]*//g' |          # remove list markers
  sed 's/\*\*\(.*?\)\*\*/\1/g' |           # bold
  sed 's/\*\*//g' |                        # remaining **
  sed 's/\*\(.*?\)\*/\1/g' |               # italic
  sed 's/\*//g' |                          # remaining *
  sed 's/[ \t]\+/ /g' |                    # normalize spaces
  sed '/./,$!d' |                          # remove leading empty lines
  sed '/^$/N;/^\n$/D' |                    # remove duplicate empty lines
  sed 's/^[ \t]*//;s/[ \t]*$//' )          # trim each line

# Website hash (exact match with copy button)
website_sha256=$(echo -n "$clean_body" | sha256sum | awk '{print $1}')

# Fuzzy social hash (one hash for X, FB, share, etc.)
fuzzy=$(echo "$clean_body" | 
  sed '/^$/d' | 
  tr '[:upper:]' '[:lower:]' | 
  sed 's/[ \t]\+/ /g' | 
  sed 's/^ //;s/ $//')

fuzzy_sha256=$(echo -n "$fuzzy" | sha256sum | awk '{print $1}')

# Git info
commit_hash=$(git rev-parse HEAD)
commit_url="https://github.com/OpenInternetManifest/Open_Internet_Manifest/commit/${commit_hash}"
commit_date=$(git log -1 --format=%cI)

# Output variables for the workflow
cat << EOF
WEBSITE_SHA256=${website_sha256}
FUZZY_SHA256=${fuzzy_sha256}
GIT_COMMIT_HASH=${commit_hash}
GIT_COMMIT_URL=${commit_url}
GIT_COMMIT_DATE=${commit_date}
EOF