#!/bin/bash

DAY="$1"
TITLE="$2"

# Body comes from a temporary file (safer)
BODY_FILE="$3"

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

cat "$BODY_FILE" >> _social-posts/en/day-${DAY}-rvn.md

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

cat "$BODY_FILE" >> _social-posts/nl/day-${DAY}-rvn.md

echo "✅ Created RVN Day ${DAY} for EN and NL"
ls -l _social-posts/en/day-${DAY}-rvn.md _social-posts/nl/day-${DAY}-rvn.md
cat _social-posts/en/day-${DAY}-rvn.md | head -n 30   # debug: show first 30 lines