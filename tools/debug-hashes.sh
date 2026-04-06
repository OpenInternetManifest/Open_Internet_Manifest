#!/bin/bash
# OIM Hash Debug Tool
# Gebruik: ./tools/debug-hashes.sh path/to/day-XX-rvn.md

FILE="$1"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 path/to/day-XX-rvn.md"
  echo "Example: $0 _social-posts/nl/day-47-rvn.md"
  exit 1
fi

echo "=== OIM Hash Debug Tool ==="
echo "File: $FILE"
echo "=================================================================="

# 1. Raw content after frontmatter
echo "1. RAW CONTENT (after frontmatter):"
raw=$(sed -n '/^---$/,/^---$/!p' "$FILE" | tail -n +2)
echo "$raw"
echo "------------------------------------------------------------------"

# 2. Website hash (exact zoals de site het zou zien)
website_hash=$(echo -n "$raw" | sha256sum | awk '{print $1}')
echo "2. website_sha256 (raw content):"
echo "$website_hash"
echo "------------------------------------------------------------------"

# 3. Fuzzy canonical text (deze gebruiken we voor alle social hashes)
fuzzy=$(echo "$raw" | \
  sed '/^$/d' | \
  sed 's/^[ \t]*//g' | \
  sed 's/[ \t]*$//g' | \
  tr -d '\r' | \
  tr '[:upper:]' '[:lower:]' | \
  sed 's/[ \t]\+/ /g')

echo "3. FUZZY CANONICAL TEXT (voor social hashes):"
echo "$fuzzy"
echo "------------------------------------------------------------------"

fuzzy_hash=$(echo -n "$fuzzy" | sha256sum | awk '{print $1}')
echo "4. Fuzzy social hash (x, fb, share):"
echo "$fuzzy_hash"
echo "------------------------------------------------------------------"

# 5. Huidige hashes uit frontmatter
echo "5. Huidige hashes in frontmatter:"
grep -E "(website_sha256|social_.*_sha256|git_commit)" "$FILE" || echo "Geen hashes gevonden"
echo "=================================================================="

echo "Klaar. Vergelijk de berekende hashes met wat er in de file staat."