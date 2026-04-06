#!/bin/bash

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "Script started with DAY=$DAY, TITLE=$TITLE"

# Clean the body aggressively: remove form headers, plus signs, empty lines, etc.
clean_body=$(cat "$BODY_FILE" | \
  sed '/^### /d' | \
  sed '/^_No response_/d' | \
  sed '/^## /d' | \
  sed 's/^\+ //g' | \
  sed '/^$/N;/^\n$/D' | \
  sed 's/^\s*//g' | \
  sed '/^nl$/d' | \
  sed '/^markdown$/d')

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

echo "✅ Successfully created clean RVN Day ${DAY} for both languages"
echo "First 40 lines of English file:"
head -n 40 _social-posts/en/day-${DAY}-rvn.md