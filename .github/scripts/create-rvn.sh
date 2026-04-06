#!/bin/bash

DAY="$1"
TITLE="$2"
BODY_FILE="$3"

echo "=== Script started ==="
echo "DAY=$DAY"
echo "TITLE=$TITLE"

# Extract Teaser
TEASER=$(awk '/### Teaser/{flag=1; next} flag && /^### /{flag=0} flag && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | tr -d '\n')

# Extract Donation link
DONATION=$(awk '/### Donatie link/{flag=1; next} flag && /^### /{flag=0} flag && NF {print}' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^_No response_$/d' | tr -d '\n')

# Extract only the real RVN content (after "Volledige RVN tekst")
clean_body=$(awk '
  /### Volledige RVN tekst \(Markdown\)/ { found=1; next }
  found && /^### / { exit }
  found { print }
' "$BODY_FILE" | \
  sed 's/^\+ //g' | \
  sed '/^```markdown$/d' | \
  sed '/^```$/d' | \
  sed '/^$/d')

# Fallback if nothing found
if [ -z "$clean_body" ]; then
  clean_body=$(cat "$BODY_FILE" | sed 's/^\+ //g' | sed '/^### /d' | sed '/^_No response_$/d' | sed '/^```/d' | sed '/^$/d')
fi

# Create files for both languages
for LANG in en nl; do
  cat > _social-posts/${LANG}/day-${DAY}-rvn.md << EOT
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
EOT
done

echo "✅ Created RVN Day ${DAY} for EN + NL"
echo "Teaser: ${TEASER:0:100}..."
echo "Donation: ${DONATION}"
echo "=== First 30 lines of English file ==="
head -n 30 _social-posts/en/day-${DAY}-rvn.md