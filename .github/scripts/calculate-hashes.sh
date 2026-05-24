#!/bin/bash
# calculate-hashes.sh - Verbeterde versie voor nieuwe + bestaande posts

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

echo "=== Processing $FILE ==="

# Extract body
raw_body=$(awk '
  BEGIN { in_body = 0 }
  /^---$/ {
    if (in_body == 0) { in_body = 1; next }
    else { in_body = 2; next }
  }
  in_body == 2 { print }
' "$FILE")

if [ ${#raw_body} -lt 100 ]; then
  raw_body=$(sed -n '/^---$/,/^---$/!p' "$FILE" | sed '/^---$/d')
fi

# 1. Generate raw_markdown if missing
if ! grep -q "^raw_markdown:" "$FILE"; then
  echo "→ Generating raw_markdown for new post..."
  # Indent with 2 spaces for YAML block scalar
  indented_body=$(echo "$raw_body" | sed 's/^/  /')
  # Insert after the opening --- block
  sed -i "/^---$/ {N; s/^\(---\)\n/\1\nraw_markdown: |\n$indented_body\n/}" "$FILE"
fi

# 2. Calculate hashes
fuzzy_body=$(python3 tools/fuzzy_clean.py <<< "$raw_body")
fuzzy_sha256=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

full_sha256=$(python3 -c '
import hashlib, re, sys
text = sys.stdin.read()
match = re.search(r"raw_markdown:\s*\|\s*\n((?:[ \t].*?\n?)+?)(?=\n[^\s]|\Z)", text, re.MULTILINE)
raw = match.group(1).rstrip("\n") if match else text
print(hashlib.sha256(raw.encode("utf-8")).hexdigest())
' < "$FILE")

# 3. Update clean texts
python3 tools/update-clean-texts.py "$FILE" "$fuzzy_body"

# 4. Update frontmatter
python3 -c '
import re, sys
file, fuzzy, full = sys.argv[1:]
with open(file, "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r"fuzzy_sha256:\s*\".*?\"", f"fuzzy_sha256: \"{fuzzy}\"", content)
content = re.sub(r"full_sha256:\s*\".*?\"", f"full_sha256: \"{full}\"", content)

if "full_sha256:" not in content:
    content = re.sub(r"(fuzzy_sha256:.*?\n)", rf"\1full_sha256: \"{full}\"\n", content)

with open(file, "w", encoding="utf-8") as f:
    f.write(content)
' "$FILE" "$fuzzy_sha256" "$full_sha256"

echo "✅ Done: $FILE"
echo "   fuzzy = $fuzzy_sha256"
echo "   full  = $full_sha256"