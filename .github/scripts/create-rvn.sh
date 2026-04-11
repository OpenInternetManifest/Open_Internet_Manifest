#!/bin/bash
# create-rvn.sh - Laatste robuuste versie (behoudt headings en newlines)

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

# Extract FULL body - zeer robuust
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ {found=1; next}
  found && /^### / && !/Volledige RVN tekst/ {exit}
  found {print}
' "$BODY_FILE")

# Verwijder alleen GitHub artifacts, behoud ALLE Markdown inclusief ###
clean_body=$(echo "$clean_body" | \
  sed 's/^\+ //g' | \
  sed '/^```markdown$/d' | \
  sed '/^```$/d' | \
  sed '/^_No response_$/d')

# Fallback als body leeg is
if [ -z "$(echo "$clean_body" | tr -d ' \n\t')" ]; then
  echo "Warning: Using full fallback"
  clean_body=$(cat "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```/d' | sed '/^_No response_$/d')
fi

echo "Body length: ${#clean_body} characters"

# Create files - gebruik heredoc met single quotes om newlines te behouden
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
  sed -i "s|LANG_PLACEHOLDER|${LANG}|" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DAY_PLACEHOLDER|${DAY}|" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TITLE_PLACEHOLDER|${TITLE}|" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TEASER_PLACEHOLDER|${TEASER}|" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DONATION_PLACEHOLDER|${DONATION}|" "_social-posts/${LANG}/day-${DAY}-rvn.md"

  # Voeg de echte body toe (behoudt alle newlines en ###)
  cat >> "_social-posts/${LANG}/day-${DAY}-rvn.md" << 'EOT2'

BODY_PLACEHOLDER
EOT2

  sed -i '/BODY_PLACEHOLDER/r /dev/stdin' "_social-posts/${LANG}/day-${DAY}-rvn.md" <<< "$clean_body"
  sed -i '/BODY_PLACEHOLDER/d' "_social-posts/${LANG}/day-${DAY}-rvn.md"

done

echo "✅ Created RVN Day ${DAY} for EN and NL"
echo "First 50 lines of NL file:"
head -n 50 "_social-posts/nl/day-${DAY}-rvn.md"