#!/bin/bash

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "Script started with DAY=$DAY, TITLE=$TITLE"

# English file - without single quotes so variables expand
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
EOT

cat "$BODY_FILE" >> _social-posts/en/day-${DAY}-rvn.md

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
EOT

cat "$BODY_FILE" >> _social-posts/nl/day-${DAY}-rvn.md

echo "✅ Successfully created RVN Day ${DAY} for both languages"
echo "First 25 lines of English file:"
head -n 25 _social-posts/en/day-${DAY}-rvn.md