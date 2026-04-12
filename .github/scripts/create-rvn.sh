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
  cat > "_social-posts/${LANG}/day-${DAY}-rvn.md" << 'EOF'
---
layout: social-posts
lang: LANG_PLACEHOLDER
day: DAY_PLACEHOLDER
rvn_title: "TITLE_PLACEHOLDER"
rvn_teaser: "TEASER_PLACEHOLDER"
donation_link: "DONATION_PLACEHOLDER"
donation_text: ""
website_sha256: ""
social_x_sha256: ""
social_fb_sha256: ""
social_share_sha256: ""
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
---

EOF

  # Voeg placeholders toe
  sed -i "s|LANG_PLACEHOLDER|${LANG}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DAY_PLACEHOLDER|${DAY}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TITLE_PLACEHOLDER|${TITLE}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TEASER_PLACEHOLDER|${TEASER}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DONATION_PLACEHOLDER|${DONATION}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"

  # Voeg de echte body toe met een extra newline voor veiligheid
  echo "" >> "_social-posts/${LANG}/day-${DAY}-rvn.md"
  cat >> "_social-posts/${LANG}/day-${DAY}-rvn.md" << 'EOT2'
BODY_PLACEHOLDER
EOT2

  sed -i '/BODY_PLACEHOLDER/r /dev/stdin' "_social-posts/${LANG}/day-${DAY}-rvn.md" <<< "$clean_body"
  sed -i '/BODY_PLACEHOLDER/d' "_social-posts/${LANG}/day-${DAY}-rvn.md"

done

echo "✅ Created RVN Day ${DAY} for EN and NL"
echo "First 60 lines of NL file:"
head -n 60 "_social-posts/nl/day-${DAY}-rvn.md"