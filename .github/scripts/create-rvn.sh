#!/bin/bash
# create-rvn.sh - Behoudt Markdown structuur beter

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="
echo "TITLE: $TITLE"

# Extract Teaser (first line after ### Teaser)
TEASER=$(awk '
  /### Teaser/ {flag=1; next}
  flag && /^### / {exit}
  flag && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | tr -d '\n' | sed 's/[ \t]+$//')

# Extract Donation link
DONATION=$(awk '
  /### Donatie link/ {flag=1; next}
  flag && /^### / {exit}
  flag && NF {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^_No response_$/d' | tr -d '\n' | sed 's/[ \t]+$//')

# Extract ONLY the real RVN body - preserve newlines and Markdown!
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ {found=1; next}
  found && /^### / {exit}
  found {print}
' "$BODY_FILE")

# Fallback if extraction failed
if [ -z "$clean_body" ]; then
  echo "Warning: Could not extract body cleanly, using fallback"
  clean_body=$(cat "$BODY_FILE")
fi

# Remove only the GitHub form artifacts (+ lines, ```markdown fences, _No response_)
clean_body=$(echo "$clean_body" | \
  sed 's/^\+ //g' | \
  sed '/^```markdown$/d' | \
  sed '/^```$/d' | \
  sed '/^_No response_$/d')

echo "Body length: ${#clean_body} characters"

# Create files for both languages - preserve exact Markdown
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

  # Replace placeholders (this way we keep newlines in body)
  sed -i "s|LANG_PLACEHOLDER|${LANG}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DAY_PLACEHOLDER|${DAY}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TITLE_PLACEHOLDER|${TITLE}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TEASER_PLACEHOLDER|${TEASER}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DONATION_PLACEHOLDER|${DONATION}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "/BODY_PLACEHOLDER/r /dev/stdin" "_social-posts/${LANG}/day-${DAY}-rvn.md" <<< "$clean_body"
  sed -i '/BODY_PLACEHOLDER/d' "_social-posts/${LANG}/day-${DAY}-rvn.md"

done

echo "✅ Created RVN Day ${DAY} for EN and NL"
echo "Teaser extracted: ${TEASER:0:80}..."
echo "First 10 lines of NL file:"
head -n 15 "_social-posts/nl/day-${DAY}-rvn.md"