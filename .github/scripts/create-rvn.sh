#!/bin/bash
# create-rvn.sh - Robuuste body extractie met behoud van Markdown opmaak

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="
echo "TITLE: $TITLE"

# Extract Teaser (eerste regel na ### Teaser)
TEASER=$(sed -n '/### Teaser/,/### /p' "$BODY_FILE" | sed '/### /d' | head -n 1 | sed 's/^[ \t+-]*//' | tr -d '\n')

# Extract Donation link (optioneel)
DONATION=$(sed -n '/### Donatie link/,/### /p' "$BODY_FILE" | sed '/### /d' | sed '/^_No response_$/d' | sed 's/^[ \t+-]*//' | tr -d '\n')

# Extract ONLY the real RVN body - alles na "Volledige RVN tekst (Markdown)" tot het einde of volgende ###
clean_body=$(sed -n '/### Volledige RVN tekst (Markdown)/,$p' "$BODY_FILE" \
  | sed '1d' \
  | sed '/### Donatie link/q' \
  | sed '/### Extra opmerkingen/q' \
  | sed 's/^[ \t+-]*//' \
  | sed '/^```markdown$/d' \
  | sed '/^```$/d' \
  | sed '/^_No response_$/d')

# Verwijder eventuele overgebleven form headers (veiligheidsnet)
clean_body=$(echo "$clean_body" | sed '/^Taal:/d' | sed '/^RVN Titel:/d' | sed '/^Teaser:/d' | sed '/^Donatie link:/d' | sed '/^Extra opmerkingen:/d')

# Zorg voor een nette lege regel na frontmatter
if [ -z "$clean_body" ]; then
  echo "⚠️  Waarschuwing: clean_body is leeg"
fi

# Maak bestanden voor beide talen
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

echo "✅ Created RVN Day ${DAY} for EN + NL"
echo "Teaser: ${TEASER:0:80}..."
echo "Donation: ${DONATION:-<none>}"
echo "=== First 60 lines of NL file ==="
head -n 60 "_social-posts/nl/day-${DAY}-rvn.md"