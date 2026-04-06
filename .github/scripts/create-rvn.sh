#!/bin/bash

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Script started ==="
echo "DAY=$DAY"
echo "TITLE=$TITLE"

# Extract only the real content after "Volledige RVN tekst (Markdown)"
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ { found=1; next }
  found && /^### / { exit }
  found { print }
' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^$/d')

# Fallback if nothing was found
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

# Dutch file
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

echo "✅ Created RVN Day ${DAY} for both languages"
echo "=== First 35 lines of English file ==="
head -n 35 _social-posts/en/day-${DAY}-rvn.md