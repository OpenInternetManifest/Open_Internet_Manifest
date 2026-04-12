#!/bin/bash
# create-rvn.sh - Tweetalige versie (NL verplicht, EN optioneel met placeholder)

DAY="$1"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="

# Extract primary language (niet echt gebruikt voor bestandskeuze, maar voor logging)
PRIMARY_LANG=$(grep -oP '(?<=primary_language: ).*' "$BODY_FILE" | head -n1 | tr -d ' ' || echo "nl")

# === Extract NL fields (verplicht) ===
TITLE_NL=$(awk '
  /### RVN Titel \(Nederlands\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

TEASER_NL=$(awk '
  /### Teaser \(Nederlands\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

BODY_NL=$(awk '
  /### Volledige RVN tekst \(Nederlands – Markdown\)/ {found=1; next}
  found && (/### Full RVN text \(English/ || /### Donatie link/ || /### Extra opmerkingen/) {exit}
  found {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

# === Extract EN fields (optioneel) ===
TITLE_EN=$(awk '
  /### RVN Title \(English\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

TEASER_EN=$(awk '
  /### Teaser \(English\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

BODY_EN_RAW=$(awk '
  /### Full RVN text \(English – Markdown\)/ {found=1; next}
  found && (/### Donatie link/ || /### Extra opmerkingen/) {exit}
  found {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

# Als BODY_EN leeg of te kort → placeholder
if [[ -z "$BODY_EN_RAW" || ${#BODY_EN_RAW} -lt 20 ]]; then
  BODY_EN="This post has not been translated into English yet.

Translation coming soon."
else
  BODY_EN="$BODY_EN_RAW"
fi

# Donation
DONATION=$(awk '
  /### Donatie link/ {found=1; next}
  found && /^### / {exit}
  found && NF {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^_No response_$/d' | sed 's/[ \t]\+$//' | tr -d '\n')

[[ -z "${DONATION// /}" ]] && DONATION=""

echo "Primary lang: $PRIMARY_LANG"
echo "Title NL: ${TITLE_NL:0:60}..."
echo "Body NL length: ${#BODY_NL}"
echo "Body EN length: ${#BODY_EN}"
echo "Donation: ${DONATION:-<none>}"

# === Create NL file ===
cat > "_social-posts/nl/day-${DAY}-rvn.md" << EOF
---
layout: social-posts
lang: nl
day: ${DAY}
rvn_title: "${TITLE_NL}"
rvn_teaser: "${TEASER_NL}"
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

${BODY_NL}
EOF

# === Create EN file ===
cat > "_social-posts/en/day-${DAY}-rvn.md" << EOF
---
layout: social-posts
lang: en
day: ${DAY}
rvn_title: "${TITLE_EN:-${TITLE_NL}}"
rvn_teaser: "${TEASER_EN:-${TEASER_NL}}"
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

${BODY_EN}
EOF

echo "✅ Created RVN Day ${DAY} for NL and EN"
echo "First 50 lines of NL file:"
head -n 50 "_social-posts/nl/day-${DAY}-rvn.md"
echo "First 30 lines of EN file:"
head -n 30 "_social-posts/en/day-${DAY}-rvn.md"