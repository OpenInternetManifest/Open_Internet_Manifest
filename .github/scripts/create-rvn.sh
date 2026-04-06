#!/bin/bash

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Script started ==="
echo "DAY=$DAY"
echo "TITLE=$TITLE"

# Extract fields from the Issue Form
TEASER=$(awk '/### Teaser/{flag=1; next} flag && /^### /{flag=0} flag {print}' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^$/d' | head -c 500)
DONATION=$(awk '/### Donatie link/{flag=1; next} flag && /^### /{flag=0} flag {print}' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^_No response_$/d' | sed '/^$/d')

# Clean main body (only the "Volledige RVN tekst" part)
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ { found=1; next }
  found && /^### / { exit }
  found { print }
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^$/d')

# Fallback if no clean body found
if [ -z "$clean_body" ]; then
  clean_body=$(cat "$BODY_FILE" | sed 's/^\+ //g' | sed '/^### /d' | sed '/^_No response_$/d' | sed '/^$/d')
fi

# English file
cat > _social-posts/en/day-${DAY}-rvn.md << EOT
---
layout: social-posts
lang: en
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
EOT

# Dutch file
cat > _social-posts/nl/day-${DAY}-rvn.md << EOT
---
layout: social-posts
lang: nl
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
EOT

echo "✅ Successfully created RVN Day ${DAY}"
echo "Teaser extracted: ${TEASER:0:100}..."
echo "Donation extracted: ${DONATION}"
echo "=== First 30 lines of English file ==="
head -n 30 _social-posts/en/day-${DAY}-rvn.md