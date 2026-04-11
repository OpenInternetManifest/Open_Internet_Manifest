#!/bin/bash
# create-rvn.sh - Zeer robuuste versie met temp file voor body

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

if [ -z "$DAY" ] || [ -z "$TITLE" ] || [ ! -f "$BODY_FILE" ]; then
  echo "Error: Ontbrekende parameters of body file"
  exit 1
fi

echo "=== Creating RVN Day $DAY ==="

# Extract Teaser
TEASER=$(awk '
  /### Teaser/ {flag=1; next}
  flag && /^### / {exit}
  flag && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | tr -d '\n' | sed 's/[ \t]\+$//')

# Extract Donation
DONATION=$(awk '
  /### Donatie link/ {flag=1; next}
  flag && /^### / {exit}
  flag && NF {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^_No response_$/d' | tr -d '\n' | sed 's/[ \t]\+$//')

# Read the FULL body as-is (behoudt alle newlines en Markdown)
BODY=$(cat "$BODY_FILE")

# Remove only GitHub artifacts
BODY=$(echo "$BODY" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

echo "Body length: ${#BODY} characters"

# Create files for both languages
for LANG in en nl; do
  cat > "_social-posts/${LANG}/day-${DAY}-rvn.md" << EOF
---
layout: social-posts
lang: ${LANG}
day: ${DAY}
rvn_title: "${TITLE}"
rvn_teaser: "${TEASER}"
donation_link: "${DONATION}"
donation_text: ""
website_sha256: ""
social_x_sha256: ""
social_fb_sha256: ""
social_share_sha256: ""
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
---
${BODY}
EOF
done

echo "✅ Created RVN Day ${DAY} for EN and NL"
echo "First 40 lines of NL file:"
head -n 40 "_social-posts/nl/day-${DAY}-rvn.md"