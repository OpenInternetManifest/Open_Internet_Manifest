#!/bin/bash

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "Script started with DAY=$DAY, TITLE=$TITLE"

# Very aggressive cleaning of the Issue Form output
clean_body=$(cat "$BODY_FILE" | \
  # Remove all lines starting with ### 
  sed '/^### /d' | \
  # Remove all lines starting with ## 
  sed '/^## /d' | \
  # Remove form field labels
  sed '/^Taal$/d' | \
  sed '/^RVN Titel$/d' | \
  sed '/^Teaser$/d' | \
  sed '/^Volledige RVN tekst (Markdown)$/d' | \
  sed '/^Donatie link (optioneel)$/d' | \
  sed '/^Extra opmerkingen voor het core team (optioneel)$/d' | \
  # Remove "No response" and empty lines
  sed '/^_No response_$/d' | \
  sed '/^nl$/d' | \
  sed '/^markdown$/d' | \
  # Remove leading + signs and extra spaces
  sed 's/^\+ //g' | \
  sed 's/^\s*//g' | \
  # Remove completely empty lines
  sed '/^$/d' | \
  # Keep only the actual content after the last form field
  tail -n +10)

# English file
cat > _social-posts/en/day-${DAY}-rvn.md << EOT
---
layout: social-posts
lang: en
day: ${DAY}
rvn_title: "${TITLE}"
rvn_teaser: ""
donation_link: ""
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
EOT

# Dutch file (same content for now)
cat > _social-posts/nl/day-${DAY}-rvn.md << EOT
---
layout: social-posts
lang: nl
day: ${DAY}
rvn_title: "${TITLE}"
rvn_teaser: ""
donation_link: ""
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
EOT

echo "✅ Successfully created RVN Day ${DAY}"
echo "=== First 40 lines of English file ==="
head -n 40 _social-posts/en/day-${DAY}-rvn.md