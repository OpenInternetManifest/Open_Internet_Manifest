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

# Stap 3: Finale body voor hashing - exact match met website (lege regel alleen bij opsomming na :)
final_body=$(echo "$body" | 
  sed 's/^>[ \t]*//g' |                    # blockquotes
  sed 's/^[ \t]*[-*+][ \t]*//g' |          # lists
  sed 's/\*\*\(.*?\)\*\*/\1/g' |           # bold
  sed 's/\*\*//g' |                        # remaining **
  sed 's/\*\(.*?\)\*/\1/g' |               # italic
  sed 's/\*//g' |                          # remaining *
  sed 's/^[ \t]*###[ \t]*//g' |            # remove ### headings
  sed 's/[ \t]\+/ /g' |                    # normalize spaces
  sed '/./,$!d' |                          # remove leading empty lines
  sed '/^$/N;/^\n$/D' |                    # remove duplicate empty lines
  # Voeg lege regel toe NA ":" ALLEEN als de volgende regel een lijst-item is
  sed '/:[ \t]*$/{
    N
    /\n[ \t]*[-*+]/ s/:\n/:\n\n/
    s/\n[ \t]*[-*+]/\n-/
  }' |
  sed 's/^[ \t]*//;s/[ \t]*$//' )          # trim each line

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