#!/bin/bash
# OIM Hash Debug Tool - Versie 27 (Algemene -- fix - schoon)

FILE="$1"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 path/to/day-XX-rvn.md"
  exit 1
fi

echo "=== OIM Hash Debug Tool - Versie 27 (Algemene -- fix) ==="
echo "File: $FILE"
echo "=================================================================="

# Stap 1: RAW BODY - volledig origineel
raw_body=$(sed '0,/^---$/d' "$FILE" | sed '0,/^---$/d')

echo "1. RAW BODY (volledig origineel):"
echo "$raw_body"
echo "------------------------------------------------------------------"

# Stap 2: WEBSITE BODY
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

echo "2. WEBSITE BODY (Markdown gestript, nette alinea-overgang i.p.v. --):"
echo "$website_body"
echo "------------------------------------------------------------------"

# Stap 3: FUZZY BODY - volledig schoon
fuzzy_body=$(echo "$website_body" | \
  tr '[:upper:]' '[:lower:]' | \
  sed '/^$/d' | \
  sed 's/[ \t]\+/ /g')

echo "3. FUZZY BODY (volledig gestript):"
echo "$fuzzy_body"
echo "------------------------------------------------------------------"

# Hashes
website_hash=$(echo -n "$website_body" | sha256sum | awk '{print $1}')
fuzzy_hash=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

echo "4. BEREKENDE HASHES:"
echo "website_sha256     : $website_hash"
echo "fuzzy social hash  : $fuzzy_hash"
echo "------------------------------------------------------------------"

echo "5. HASHES IN FRONTMATTER:"
grep -E "(website_sha256|social_.*_sha256)" "$FILE" || echo "Geen hashes gevonden"

echo "=================================================================="
echo "Kopieer WEBSITE BODY (stap 2) voor online SHA256 tool."