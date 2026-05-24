#!/bin/bash
# rebuild-clean-texts.sh - Verzamelt alles en schrijft JS in één keer

echo "=== Starting full rebuild of official-clean-texts.js ==="

JS_FILE="static/js/official-clean-texts.js"

# Start structuur
cat > "$JS_FILE" << 'EOF'
// ==================== OFFICIAL FUZZY HASHES + CLEAN TEXTS ====================
// Auto generated - $(date)

window.officialFuzzyHashes = {};
window.officialCleanTexts = {};

EOF

# Verzamel alle hashes en clean texts
echo "Processing posts..."

for file in $(find _social-posts -name "day-*.md" | sort); do
    echo "→ $file"
    ./.github/scripts/calculate-hashes.sh "$file" > /dev/null
done

echo "=== Rebuild finished ==="
echo "Total lines in JS: $(wc -l < "$JS_FILE")"