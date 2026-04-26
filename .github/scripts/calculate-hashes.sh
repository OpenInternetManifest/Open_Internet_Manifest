#!/bin/bash
# calculate-hashes.sh - Updated with unified fuzzy_clean (same as fix-all + debug)

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE"
  exit 1
fi

# Extract body after frontmatter
raw_body=$(sed '0,/^---$/d' "$FILE" | sed '0,/^---$/d')

# ==================== FUZZY CLEAN (PYTHON-STYLE) ====================
fuzzy_body=$(python3 - <<EOF
import sys
import re
import unicodedata

text = """$raw_body"""

# Exact same fuzzy_clean as in fix-all-fuzzy-hashes.py
text = unicodedata.normalize('NFKC', text)

# Emoji's verwijderen
emoji_pattern = re.compile(
    "[" 
    "\U0001F600-\U0001F64F"  
    "\U0001F300-\U0001F5FF"  
    "\U0001F680-\U0001F6FF"  
    "\U0001F1E0-\U0001F1FF"  
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "]+", flags=re.UNICODE)
text = emoji_pattern.sub('', text)

# Markdown & formatting
text = re.sub(r'\*\*(.*?)\*\*', r'\1', text, flags=re.DOTALL)
text = re.sub(r'__(.*?)__', r'\1', text, flags=re.DOTALL)
text = re.sub(r'\*(.*?)\*', r'\1', text, flags=re.DOTALL)
text = re.sub(r'_(.*?)_', r'\1', text, flags=re.DOTALL)

text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
text = re.sub(r'^\s*[-*+]\s+', ' ', text, flags=re.MULTILINE)
text = re.sub(r'^\s*\d+\.\s+', ' ', text, flags=re.MULTILINE)
text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
text = re.sub(r'`([^`]+)`', r'\1', text)
text = re.sub(r'^-{3,}\s*$', ' ', text, flags=re.MULTILINE)

# HTML
text = re.sub(r'<[^>]+>', '', text)

# Selectieve colon cleanup
title_colons = r'(narratief|realiteit|hoe werkt het|hoe zien we dit|de grote verbinding|de oim-boodschap|traumabinding|cognitive dissonance|identificatie|overheid en burgers|social media|relaties en sekten|politiek|dank dat je|lees zelf|check zelf|weiger mee te spelen|schokkends|en vooral)'
text = re.sub(rf'({title_colons})\s*:\s*', r'\1 ', text, flags=re.IGNORECASE)

# URLs beschermen + overige colons
text = re.sub(r'https?://', '___URL___', text)
text = re.sub(r':', ' ', text)
text = re.sub(r'___URL___', 'https://', text)

# Whitespace + lowercase
text = re.sub(r'\s+', ' ', text)
text = text.strip().lower()

print(text, end='')
EOF
)

fuzzy_sha256=$(echo -n "$fuzzy_body" | sha256sum | awk '{print $1}')

# Git info
commit_hash=$(git rev-parse HEAD)
commit_url="https://github.com/OpenInternetManifest/Open_Internet_Manifest/commit/${commit_hash}"
commit_date=$(git log -1 --format=%cI)

# Output voor GitHub Actions
cat << EOF
fuzzy_sha256=${fuzzy_sha256}
GIT_COMMIT_HASH=${commit_hash}
GIT_COMMIT_URL=${commit_url}
GIT_COMMIT_DATE=${commit_date}
EOF

echo "✅ Fuzzy hash calculated for $(basename "$FILE")" >&2