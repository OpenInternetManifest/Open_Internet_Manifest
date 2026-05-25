#!/bin/bash
# create-rvn.sh - Maakt NL + EN bestanden met raw_markdown in frontmatter

DAY="$1"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="

# Extract fields
TITLE_NL=$(awk '/### RVN Titel \(Nederlands\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')
TEASER_NL=$(awk '/### Teaser \(Nederlands\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

BODY_NL=$(awk '/### Volledige RVN tekst \(Nederlands – Markdown\)/ {found=1; next} found && (/### Full RVN text/ || /### Donatie link/) {exit} found {print}' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

TITLE_EN=$(awk '/### RVN Title \(English\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')
TEASER_EN=$(awk '/### Teaser \(English\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

BODY_EN=$(awk '/### Full RVN text \(English – Markdown\)/ {found=1; next} found && /### Donatie link/ {exit} found {print}' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

# Placeholders
[[ -z "$TITLE_EN" ]] && TITLE_EN="This post has not been translated into English yet."
[[ -z "$TEASER_EN" ]] && TEASER_EN="Translation coming soon."
[[ -z "$BODY_EN" ]] && BODY_EN="This post has not been translated into English yet.\n\nTranslation coming soon."

# === Create NL file with raw_markdown ===
cat > "_social-posts/nl/day-${DAY}-rvn.md" << EOF
---
layout: social-posts
lang: nl
day: ${DAY}
rvn_title: "${TITLE_NL}"
rvn_teaser: "${TEASER_NL}"
donation_link: ""
donation_text: ""
fuzzy_sha256: ""
full_sha256: ""
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
raw_markdown: |
$(echo "${BODY_NL}" | sed 's/^/  /')
---

${BODY_NL}
EOF

# === Create EN file ===
cat > "_social-posts/en/day-${DAY}-rvn.md" << EOF
---
layout: social-posts
lang: en
day: ${DAY}
rvn_title: "${TITLE_EN}"
rvn_teaser: "${TEASER_EN}"
donation_link: ""
donation_text: ""
fuzzy_sha256: ""
full_sha256: ""
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
raw_markdown: |
$(echo "${BODY_EN}" | sed 's/^/  /')
---

${BODY_EN}
EOF

echo "✅ Created RVN Day ${DAY} with raw_markdown in frontmatter"
head -n 35 "_social-posts/nl/day-${DAY}-rvn.md"