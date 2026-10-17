#!/bin/bash
# OIM Hash Debug Tool - Versie 42 (Zeer fuzzy - alles op 1 regel)

FILE="$1"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 path/to/day-XX-rvn.md"
  exit 1
fi

echo "=== OIM Hash Debug Tool - Versie 42 (Zeer fuzzy) ==="
echo "File: $FILE"
echo "=================================================================="

# RAW BODY
raw_body=$(sed '0,/^---$/d' "$FILE" | sed '0,/^---$/d')

echo "1. RAW BODY (volledig origineel):"
echo "$raw_body"
echo "------------------------------------------------------------------"

# FUZZY BODY - zeer fuzzy (alles op 1 regel, geen witregels)
fuzzy_body=$(echo "$raw_body" | \
  sed 's/\*\*\(.*?\)\*\*/\1/g' | \
  sed 's/\*\(.*?\)\*/\1/g' | \
  sed 's/\*\*//g' | \
  sed 's/\*//g' | \
  sed 's/^>[ \t]*//g' | \
  sed 's/^[ \t]*###*[ \t]*//g' | \
  sed 's/^[ \t]*[0-9]\+\.[ \t]*//g' | \
  sed 's/^[ \t]*[-*+][ \t]*//g' | \
  sed 's/^[ \t]*//g' | \
  sed 's/[ \t]*$//g' | \
  sed '/^--$/d' | \
  sed '/^---$/d' | \
  sed 's/| / /g' | \
  sed 's/ |/ /g' | \
  sed '/^[-:| ]*$/d' | \
  tr '[:upper:]' '[:lower:]' | \
  sed 's/[ \t]\+/ /g' | \
  tr '\n' ' ' | \
  sed 's/[ \t]\+/ /g' | \
  sed 's/^ //;s/ $//' )

echo "2. FUZZY BODY (zeer fuzzy - alles op 1 regel):"
echo "$fuzzy_body"
echo "------------------------------------------------------------------"

# Hash
fuzzy_hash=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

echo "3. BEREKENDE HASH:"
echo "fuzzy_sha256 : $fuzzy_hash"
echo "------------------------------------------------------------------"

echo "5. HASHES IN FRONTMATTER:"
grep -E "(website_sha256|social_.*_sha256)" "$FILE" || echo "Geen hashes gevonden"

echo "=================================================================="
echo "Kopieer FUZZY BODY voor online SHA256 tool (of plak in hash-verifier)."