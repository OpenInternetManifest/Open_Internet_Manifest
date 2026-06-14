#!/bin/bash
# create-rvn.sh - Maakt NL + EN RVN met raw_markdown, clean_text + hashes

DAY="$1"
BODY_FILE="$3"

echo "=== Creating RVN Day $DAY ==="

# === Velden extraheren ===
TITLE_NL=$(awk '/### RVN Titel \(Nederlands\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')
TEASER_NL=$(awk '/### Teaser \(Nederlands\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

BODY_NL=$(awk '/### Volledige RVN tekst \(Nederlands – Markdown\)/ {found=1; next} found && (/### Full RVN text/ || /### Donatie link/) {exit} found {print}' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

TITLE_EN=$(awk '/### RVN Title \(English\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')
TEASER_EN=$(awk '/### Teaser \(English\)/ {found=1; next} found && /^### / {exit} found && NF {print; exit}' "$BODY_FILE" | sed 's/^\+ //g' | sed 's/[ \t]\+$//')

BODY_EN=$(awk '/### Full RVN text \(English – Markdown\)/ {found=1; next} found && /### Donatie link/ {exit} found {print}' "$BODY_FILE" | sed 's/^\+ //g' | sed '/^```markdown$/d' | sed '/^```$/d' | sed '/^_No response_$/d')

# Placeholders Engels
[[ -z "$TITLE_EN" ]] && TITLE_EN="This post has not been translated into English yet."
[[ -z "$TEASER_EN" ]] && TEASER_EN="Translation coming soon."
[[ -z "$BODY_EN" ]] && BODY_EN="This post has not been translated into English yet.\n\nTranslation coming soon."

# === Clean_text genereren ===
CLEAN_NL=$(echo "$BODY_NL" | python3 tools/fuzzy_clean.py)
CLEAN_EN=$(echo "$BODY_EN" | python3 tools/fuzzy_clean.py)

# === Hashes berekenen ===
FULL_SHA_NL=$(echo "$BODY_NL" | python3 -c '
import sys
import hashlib
print(hashlib.sha256(sys.stdin.read().encode("utf-8")).hexdigest())
')
FUZZY_SHA_NL=$(echo "$CLEAN_NL" | python3 -c '
import sys
import hashlib
print(hashlib.sha256(sys.stdin.read().encode("utf-8")).hexdigest())
')

FULL_SHA_EN=$(echo "$BODY_EN" | python3 -c '
import sys
import hashlib
print(hashlib.sha256(sys.stdin.read().encode("utf-8")).hexdigest())
')
FUZZY_SHA_EN=$(echo "$CLEAN_EN" | python3 -c '
import sys
import hashlib
print(hashlib.sha256(sys.stdin.read().encode("utf-8")).hexdigest())
')

# === NL bestand aanmaken ===
cat > "_social-posts/nl/day-${DAY}-rvn.md" << EOF
---
layout: social-posts
lang: nl
day: ${DAY}
rvn_title: "${TITLE_NL}"
rvn_teaser: "${TEASER_NL}"
donation_link: ""
donation_text: ""

raw_markdown: |
$(echo "${BODY_NL}" | sed 's/^/  /')

clean_text: |-
$(echo "${CLEAN_NL}" | sed 's/^/  /')

full_sha256: ${FULL_SHA_NL}
fuzzy_sha256: ${FUZZY_SHA_NL}
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
---

${BODY_NL}
EOF

# === EN bestand aanmaken ===
cat > "_social-posts/en/day-${DAY}-rvn.md" << EOF
---
layout: social-posts
lang: en
day: ${DAY}
rvn_title: "${TITLE_EN}"
rvn_teaser: "${TEASER_EN}"
donation_link: ""
donation_text: ""

raw_markdown: |
$(echo "${BODY_EN}" | sed 's/^/  /')

clean_text: |-
$(echo "${CLEAN_EN}" | sed 's/^/  /')

full_sha256: ${FULL_SHA_EN}
fuzzy_sha256: ${FUZZY_SHA_EN}
git_commit_hash: ""
git_commit_url: ""
git_commit_date: ""
---

${BODY_EN}
EOF

echo "✅ Created RVN Day ${DAY} with raw_markdown + clean_text + hashes"
echo "   NL  → full: ${FULL_SHA_NL:0:12}... | fuzzy: ${FUZZY_SHA_NL:0:12}..."
echo "   EN  → full: ${FULL_SHA_EN:0:12}... | fuzzy: ${FUZZY_SHA_EN:0:12}..."