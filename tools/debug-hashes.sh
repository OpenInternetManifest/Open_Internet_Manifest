#!/bin/bash
# OIM Hash Debug Tool - Robuuste versie
# Gebruik: ./tools/debug-hashes.sh _social-posts/nl/day-49-rvn.md

FILE="$1"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 path/to/day-XX-rvn.md"
  exit 1
fi

echo "=== OIM Hash Debug Tool ==="
echo "File: $FILE"
echo "=================================================================="

# Verwijder Git diff + tekens en extract pure content na frontmatter
raw=$(sed 's/^\+ //' "$FILE" | \
      sed -n '/^---$/,/^---$/!p' | \
      tail -n +2 | \
      sed '/^$/d')

echo "1. RAW CONTENT (after frontmatter):"
echo "$raw"
echo "------------------------------------------------------------------"

# Website hash (exact zoals Jekyll het zou renderen)
website_hash=$(echo -n "$raw" | sha256sum | awk '{print $1}')
echo "2. website_sha256 (raw content):"
echo "$website_hash"
echo "------------------------------------------------------------------"

# Fuzzy canonical text voor alle social platforms
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

# Toon huidige frontmatter hashes
echo "5. Huidige hashes in frontmatter:"
grep -E "(rvn_title|rvn_teaser|donation_link|website_sha256|social_.*_sha256|git_commit)" "$FILE"

echo "=================================================================="
echo "Vergelijking klaar."
echo "Als de berekende hashes overeenkomen met de file, is alles correct."