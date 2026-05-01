#!/bin/bash
# calculate-hashes.sh - Fuzzy + automatic official-clean-texts.js update

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

# ==================== BETERE BODY EXTRACTION ====================
raw_body=$(awk '
  BEGIN { in_body = 0 }
  /^---$/ {
    if (in_body == 0) { in_body = 1; next }
    else { in_body = 2; next }
  }
  in_body == 2 { print }
' "$FILE")

# Fallback
if [ ${#raw_body} -lt 500 ]; then
  raw_body=$(sed -n '/^---$/,/^---$/!p' "$FILE" | sed '/^---$/d')
fi

# ==================== FUZZY CLEAN ====================
fuzzy_body=$(python3 -c '
import sys
import re
import unicodedata

text = sys.stdin.read()

def fuzzy_clean(t):
    if not t: return ""
    t = unicodedata.normalize("NFKC", t)
    
    emoji_pattern = re.compile("[" 
        "\U0001F600-\U0001F64F"  
        "\U0001F300-\U0001F5FF"  
        "\U0001F680-\U0001F6FF"  
        "\U0001F1E0-\U0001F1FF"  
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "]+", flags=re.UNICODE)
    t = emoji_pattern.sub("", t)
    
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"__(.*?)__", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"\*(.*?)\*", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"_(.*?)_", r"\1", t, flags=re.DOTALL)
    
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^>\s*", "", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*[-*+]\s+", " ", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*\d+\.\s+", " ", t, flags=re.MULTILINE)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"!\[.*?\]\(.*?\)", "", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"^-{3,}\s*$", " ", t, flags=re.MULTILINE)
    t = re.sub(r"<[^>]+>", "", t)
    
    title_colons = r"(narratief|realiteit|hoe werkt het|hoe zien we dit|de grote verbinding|de oim-boodschap|traumabinding|cognitive dissonance|identificatie|overheid en burgers|social media|relaties en sekten|politiek|dank dat je|lees zelf|check zelf|weiger mee te spelen|schokkends|en vooral)"
    t = re.sub(rf"({title_colons})\s*:\s*", r"\1 ", t, flags=re.IGNORECASE)
    
    t = re.sub(r"https?://", "___URL___", t)
    t = re.sub(r":", " ", t)
    t = re.sub(r"___URL___", "https://", t)
    
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

print(fuzzy_clean(text), end="")
' <<< "$raw_body")

fuzzy_sha256=$(echo -n "$fuzzy_body" | sha256sum | awk "{print \$1}")

# ==================== UPDATE official-clean-texts.js ====================
CLEAN_FILE="static/js/official-clean-texts.js"

# Zorg dat map en bestand bestaan
mkdir -p static/js

if [ ! -f "$CLEAN_FILE" ]; then
  cat > "$CLEAN_FILE" << 'EOF'
// ==================== OFFICIAL CLEAN TEXTS ====================
// Gegenereerd op: $(date)

window.officialCleanTexts = {
};
EOF
fi

# Escape voor veilige JS string
escaped_clean=$(echo "$fuzzy_body" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')

# Verwijder oude entry als die bestaat en voeg nieuwe toe
temp_file=$(mktemp)
awk -v key="$FILE" -v value="$escaped_clean" '
  BEGIN { found = 0 }
  $0 ~ "^  \"" key "\":" { 
    print "  \"" key "\": \"" value "\",";
    found = 1;
    next 
  }
  { print }
  END {
    if (found == 0) {
      # Voeg toe voor de laatste }
      while (getline < "'"$CLEAN_FILE"'") {
        if ($0 ~ /^\};$/) {
          print "  \"" key "\": \"" value "\",";
        }
        print
      }
    }
  }
' "$CLEAN_FILE" > "$temp_file" 2>/dev/null || cp "$CLEAN_FILE" "$temp_file"

# Veilig overschrijven
mv "$temp_file" "$CLEAN_FILE"

echo "=== DEBUG: Added/updated clean text for $FILE in official-clean-texts.js ===" >&2
# ==================== DEBUG + OUTPUT ====================
echo "=== DEBUG: Raw body length = ${#raw_body} ===" >&2
echo "=== DEBUG: Cleaned length = ${#fuzzy_body} ===" >&2
echo "=== DEBUG: fuzzy_sha256 = $fuzzy_sha256 ===" >&2
echo "=== DEBUG: Added/updated clean text for $FILE in official-clean-texts.js ===" >&2

commit_hash=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
commit_url="https://github.com/OpenInternetManifest/Open_Internet_Manifest/commit/${commit_hash}"
commit_date=$(git log -1 --format=%cI 2>/dev/null || echo "unknown")

cat << EOF
fuzzy_sha256=${fuzzy_sha256}
GIT_COMMIT_HASH=${commit_hash}
GIT_COMMIT_URL=${commit_url}
GIT_COMMIT_DATE=${commit_date}
EOF