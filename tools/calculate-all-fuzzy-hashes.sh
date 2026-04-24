#!/bin/bash
# OIM - Ultra Simple Fuzzy Hash Updater v1.7
# Gebruikt awk om frontmatter en body strikt te scheiden

FILE="$1"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 path/to/day-59-rvn.md"
  exit 1
fi

echo "=== OIM Ultra Simple Fuzzy Hash Updater v1.7 ==="
echo "File: $FILE"

# Use awk to split frontmatter and body cleanly
frontmatter=$(awk '
  NR == 1 && $0 == "---" { in_front=1; print; next }
  in_front && $0 == "---" { print; in_front=0; next }
  in_front { print }
' "$FILE")

body=$(awk '
  BEGIN { found=0 }
  $0 == "---" { if (found) { print; exit } else { found=1; next } }
  found { print }
' "$FILE")

# Calculate fuzzy hash from body
fuzzy_body=$(echo "$body" | \
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
  sed 's/^ //;s/ $//')

fuzzy_hash=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

echo "Calculated fuzzy_sha256: $fuzzy_hash"

# Clean frontmatter (remove old fuzzy_sha256)
clean_frontmatter=$(echo "$frontmatter" | sed '/^fuzzy_sha256:/d')

# Rebuild the file
{
  echo "$clean_frontmatter"
  echo "fuzzy_sha256: \"${fuzzy_hash}\""
  echo "---"
  echo "$body"
} > "$FILE.tmp"

mv "$FILE.tmp" "$FILE"

echo "✅ File rebuilt with clean frontmatter + ONE fuzzy_sha256"
echo "First 40 lines:"
head -n 40 "$FILE"
echo "=================================================================="
echo "Done!"