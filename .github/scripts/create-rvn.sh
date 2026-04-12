#!/bin/bash
# create-rvn.sh - Robuuste versie met betere teaser extractie

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="
echo "TITLE: $TITLE"

# === Extract Teaser (veel robuuster) ===
TEASER=$(awk '
  /### Teaser/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}   # pak de eerste niet-lege regel na ### Teaser
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//' | tr -d '\n')

# Extract Donation - alleen echte waarde als ingevuld
DONATION=$(awk '
  /### Donatie link/ {found=1; next}
  found && /^### / {exit}
  found && NF {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^_No response_$/d' | sed 's/[ \t]\+$//' | tr -d '\n')

# Als DONATION leeg is of alleen whitespace, maak het echt leeg
if [[ -z "${DONATION// /}" ]]; then
  DONATION=""
fi

# === Extract ONLY the real body ===
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ {found=1; next}
  found && (/### Donatie link/ || /### Extra opmerkingen/) {exit}
  found {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

echo "Teaser length: ${#TEASER} characters"
echo "Donation: ${DONATION:-<none>}"
echo "Body length: ${#clean_body} characters"

# Create files for both languages
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

  # Vervang placeholders
  sed -i "s|LANG_PLACEHOLDER|${LANG}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DAY_PLACEHOLDER|${DAY}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TITLE_PLACEHOLDER|${TITLE}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TEASER_PLACEHOLDER|${TEASER}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DONATION_PLACEHOLDER|${DONATION}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"

  # Voeg body toe met veilige newline
  echo "" >> "_social-posts/${LANG}/day-${DAY}-rvn.md"
  cat >> "_social-posts/${LANG}/day-${DAY}-rvn.md" << 'EOT2'
BODY_PLACEHOLDER
EOT2

  sed -i '/BODY_PLACEHOLDER/r /dev/stdin' "_social-posts/${LANG}/day-${DAY}-rvn.md" <<< "$clean_body"
  sed -i '/BODY_PLACEHOLDER/d' "_social-posts/${LANG}/day-${DAY}-rvn.md"

done

echo "✅ Created RVN Day ${DAY} for EN and NL"
echo "First 70 lines of NL file:"
head -n 70 "_social-posts/nl/day-${DAY}-rvn.md"