#!/bin/bash
# create-rvn.sh - Betere Markdown behoud + robuuste body extractie

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="
echo "TITLE: $TITLE"

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

# Extract FULL RVN body - stop alleen bij een nieuwe ### sectie die NIET de body zelf is
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ {found=1; next}
  found && /^### / && !/Volledige RVN tekst/ {exit}
  found {print}
' "$BODY_FILE")

# Fallback als extractie faalt
if [ -z "$(echo "$clean_body" | tr -d ' \n\t')" ]; then
  echo "Warning: Body extraction failed, using fallback"
  clean_body=$(cat "$BODY_FILE")
fi

# Verwijder alleen GitHub-form artifacts, behoud alle Markdown en newlines
clean_body=$(echo "$clean_body" | \
  sed 's/^\+ //g' | \
  sed '/^```markdown$/d' | \
  sed '/^```$/d' | \
  sed '/^_No response_$/d')

echo "Body length: ${#clean_body} characters"

# Create files - preserve exact newlines and Markdown
for LANG in en nl; do
  cat > "_social-posts/${LANG}/day-${DAY}-rvn.md" << 'EOT'
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
BODY_PLACEHOLDER
EOT

  # Replace placeholders
  sed -i "s|LANG_PLACEHOLDER|${LANG}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DAY_PLACEHOLDER|${DAY}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TITLE_PLACEHOLDER|${TITLE}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TEASER_PLACEHOLDER|${TEASER}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DONATION_PLACEHOLDER|${DONATION}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"

  # Insert the real body while preserving all newlines
  sed -i '/BODY_PLACEHOLDER/r /dev/stdin' "_social-posts/${LANG}/day-${DAY}-rvn.md" <<< "$clean_body"
  sed -i '/BODY_PLACEHOLDER/d' "_social-posts/${LANG}/day-${DAY}-rvn.md"

done

echo "✅ Created RVN Day ${DAY} for EN and NL"
echo "Teaser: ${TEASER:0:100}..."
echo "First 20 lines of NL file:"
head -n 20 "_social-posts/nl/day-${DAY}-rvn.md"