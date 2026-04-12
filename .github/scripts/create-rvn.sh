#!/bin/bash
# create-rvn.sh - Tweetalige versie (NL verplicht, EN optioneel met placeholder)

DAY="$1"
TITLE="$2"          # Dit is nu niet meer in gebruik (we gebruiken _nl en _en)
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="

# === Extract fields from the new bilingual form ===
PRIMARY_LANG=$(awk -F': ' '/primary_language:/ {print $2; exit}' "$BODY_FILE" | tr -d ' ')

RVN_TITLE_NL=$(awk '
  /### RVN Titel \(Nederlands\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

RVN_TITLE_EN=$(awk '
  /### RVN Title \(English\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

TEASER_NL=$(awk '
  /### Teaser \(Nederlands\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

TEASER_EN=$(awk '
  /### Teaser \(English\)/ {found=1; next}
  found && /^### / {exit}
  found && NF {print; exit}
' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

DONATION=$(awk '
  /### Donatie link/ {found=1; next}
  found && /^### / {exit}
  found && NF {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^_No response_$/d' | sed 's/[ \t]\+$//' | tr -d '\n')

# Als DONATION leeg is → echt leeg maken
[[ -z "${DONATION// /}" ]] && DONATION=""

# === Extract body NL (verplicht) ===
BODY_NL=$(awk '
  /### Volledige RVN tekst \(Nederlands/ {found=1; next}
  found && (/### Volledige RVN tekst \(English/ || /### Donatie link/ || /### Extra opmerkingen/) {exit}
  found {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

# === Extract body EN (optioneel) ===
BODY_EN=$(awk '
  /### Full RVN text \(English/ {found=1; next}
  found && (/### Donatie link/ || /### Extra opmerkingen/) {exit}
  found {print}
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

# Als BODY_EN leeg is → placeholder
if [[ -z "$BODY_EN" || "${#BODY_EN}" -lt 10 ]]; then
  BODY_EN="This post has not been translated into English yet.

Translation coming soon."
fi

echo "Primary language: ${PRIMARY_LANG:-nl}"
echo "Title NL length: ${#RVN_TITLE_NL}"
echo "Title EN length: ${#RVN_TITLE_EN}"
echo "Teaser NL length: ${#TEASER_NL}"
echo "Body NL length: ${#BODY_NL}"
echo "Body EN length: ${#BODY_EN}"
echo "Donation: ${DONATION:-<none>}"

# === Create files ===
for LANG in nl en; do
  if [[ "$LANG" == "nl" ]]; then
    TITLE_TO_USE="${RVN_TITLE_NL}"
    TEASER_TO_USE="${TEASER_NL}"
    BODY_TO_USE="${BODY_NL}"
  else
    TITLE_TO_USE="${RVN_TITLE_EN:-${RVN_TITLE_NL}}"
    TEASER_TO_USE="${TEASER_EN:-${TEASER_NL}}"
    BODY_TO_USE="${BODY_EN}"
  fi

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
  sed -i "s|TITLE_PLACEHOLDER|${TITLE_TO_USE}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|TEASER_PLACEHOLDER|${TEASER_TO_USE}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"
  sed -i "s|DONATION_PLACEHOLDER|${DONATION}|g" "_social-posts/${LANG}/day-${DAY}-rvn.md"

  # Voeg body toe
  echo "" >> "_social-posts/${LANG}/day-${DAY}-rvn.md"
  cat >> "_social-posts/${LANG}/day-${DAY}-rvn.md" << 'EOT2'
BODY_PLACEHOLDER
EOT2

  sed -i '/BODY_PLACEHOLDER/r /dev/stdin' "_social-posts/${LANG}/day-${DAY}-rvn.md" <<< "$BODY_TO_USE"
  sed -i '/BODY_PLACEHOLDER/d' "_social-posts/${LANG}/day-${DAY}-rvn.md"

done

echo "✅ Created RVN Day ${DAY} for NL and EN"
echo "First 60 lines of NL file:"
head -n 60 "_social-posts/nl/day-${DAY}-rvn.md"