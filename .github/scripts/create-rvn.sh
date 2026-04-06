#!/bin/bash

DAY="$1"
TITLE="$2"
BODY="$3"

# English file
cat > _social-posts/en/day-${DAY}-rvn.md << 'EOT'
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

# Append the body safely
printf '%s\n' "$BODY" >> _social-posts/en/day-${DAY}-rvn.md

# Dutch file
cat > _social-posts/nl/day-${DAY}-rvn.md << 'EOT'
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

printf '%s\n' "$BODY" >> _social-posts/nl/day-${DAY}-rvn.md

echo "✅ Created RVN Day ${DAY} for EN and NL"
ls -l _social-posts/en/day-${DAY}-rvn.md _social-posts/nl/day-${DAY}-rvn.md