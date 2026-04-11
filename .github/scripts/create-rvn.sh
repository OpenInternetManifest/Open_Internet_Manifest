#!/bin/bash
# create-rvn.sh - Definitieve versie: stopt strikt na de body

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="
echo "TITLE: $TITLE"

# Extract Teaser
TEASER=$(grep -A 5 "### Teaser" "$BODY_FILE" | grep -v "^### " | head -n 1 | sed 's/^\+ //g' | tr -d '\n' | sed 's/[ \t]\+$//')

# Extract Donation
DONATION=$(grep -A 3 "### Donatie link" "$BODY_FILE" | grep -v "^### " | sed '/^_No response_$/d' | sed 's/^\+ //g' | tr -d '\n' | sed 's/[ \t]\+$//')

# Extract ONLY the real RVN body - stop bij de eerste optionele sectie na de body
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ {found=1; next}
  found && (/### Donatie link/ || /### Extra opmerkingen/) {exit}
  found {print}
' "$BODY_FILE")

# Verwijder GitHub artifacts
clean_body=$(echo "$clean_body" | \
  sed 's/^\+ //g' | \
  sed '/^```markdown$/d' | \
  sed '/^```$/d' | \
  sed '/^_No response_$/d')

echo "Body length: ${#clean_body} characters"

# Create files
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
${clean_body}
EOF
done

echo "✅ Created RVN Day ${DAY} for EN and NL"
echo "First 60 lines of NL file:"
head -n 60 "_social-posts/nl/day-${DAY}-rvn.md"