#!/usr/bin/env bash
# replace-body-dashes.sh - Duidelijke en betrouwbare versie

set -euo pipefail

EM="————————————"
BASE="_social-posts"
FIXED=0

echo "🔍 Zoeken naar --- in body..."

for lang in nl en; do
    for file in "$BASE/$lang"/day-*.md; do
        [ -f "$file" ] || continue

        # Tel echte losse --- in de body
        body_hr=$(awk '/^---$/{fm++} fm>=2 && /^[[:space:]]*---[[:space:]]*$/' "$file" | wc -l)

        if [ "$body_hr" -gt 0 ]; then
            cp "$file" "${file}.bak_hr"

            awk -v em="$EM" '
                BEGIN { fm = 0 }
                /^---$/ { fm++; print; next }
                {
                    if (fm >= 2 && $0 ~ /^[[:space:]]*---[[:space:]]*$/) {
                        print em
                    } else {
                        print
                    }
                }
            ' "$file" > "${file}.tmp"

            mv "${file}.tmp" "$file"
            echo "✅ Fixed $body_hr HR in: $(basename "$file")"
            FIXED=$((FIXED + 1))
        fi
    done
done

echo -e "\nKlaar! $FIXED bestanden hadden --- in de body en zijn gefixt."
echo "Backups: *.bak_hr"