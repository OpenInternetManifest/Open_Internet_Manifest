#!/bin/bash
# OIM Live Hash Debug Tool - Definitief (betere Markdown stripping)

FILE="$1"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 path/to/day-XX-rvn.md"
  exit 1
fi

echo "=== OIM Live Hash Debug Tool - DEFINITIEF (Markdown strip v2) ==="
echo "File: $FILE"
echo "=================================================================="

# Stap 1: Volledige raw
echo "STAP 1: Volledige raw bestand:"
cat "$FILE"
echo "------------------------------------------------------------------"

# Stap 2: Pure body na frontmatter
body=$(sed '0,/^[ \t]*---[ \t]*$/d' "$FILE" | sed '0,/^[ \t]*---[ \t]*$/d')

echo "STAP 2: Pure body na frontmatter (raw):"
echo "$body"
echo "------------------------------------------------------------------"

# Stap 3: Finale body - STRIP MARKDOWN + sluitende **
final_body=$(echo "$body" | 
  # Verwijder blockquotes
  sed 's/^>[ \t]*//g' |
  # Verwijder lijst-items
  sed 's/^[ \t]*[-*+][ \t]*//g' |
  # Verwijder bold **text** en losse ** aan eind van regels
  sed 's/\*\*\(.*?\)\*\*/\1/g' |
  sed 's/\*\*//g' |
  # Verwijder italic *text*
  sed 's/\*\(.*?\)\*/\1/g' |
  sed 's/\*//g' |
  # Normaliseer spaties
  sed 's/[ \t]\+/ /g' |
  # Verwijder overtollige lege regels
  sed '/./,$!d' |
  sed '/^$/N;/^\n$/D' |
  sed 's/^[ \t]*//;s/[ \t]*$//' )

echo "STAP 3: Finale body voor hashing (Markdown volledig gestript):"
echo "$final_body"
echo "------------------------------------------------------------------"

# Hashes
website_hash=$(echo -n "$final_body" | sha256sum | awk '{print $1}')

fuzzy=$(echo "$final_body" | 
  sed '/^$/d' | 
  tr '[:upper:]' '[:lower:]' | 
  sed 's/[ \t]\+/ /g' | 
  sed 's/^ //;s/ $//')

fuzzy_hash=$(echo -n "$fuzzy" | sha256sum | awk '{print $1}')

echo "4. BEREKENDE HASHES:"
echo "website_sha256     : $website_hash"
echo "fuzzy social hash  : $fuzzy_hash"
echo "------------------------------------------------------------------"

echo "5. HASHES IN FRONTMATTER:"
grep -E "(website_sha256|social_.*_sha256)" "$FILE"

echo "=================================================================="
echo "Einde debug. Kopieer STAP 3 en plak in online SHA tool."