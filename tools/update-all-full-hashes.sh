#!/bin/bash
# tools/update-all-full-hashes.sh

MODE=$1  # dry of update

echo "=== Full SHA256 Updater started ==="

for dir in nl en; do
    echo -e "\n→ Processing _social-posts/$dir ..."

    total=0
    updated=0
    skipped=0

    for file in _social-posts/$dir/*.md; do
        [ -f "$file" ] || continue
        total=$((total + 1))

        if [ "$MODE" = "update" ]; then
            python3 tools/update-full-hash.py "$file" --update
            if [ $? -eq 0 ]; then
                updated=$((updated + 1))
            else
                skipped=$((skipped + 1))
            fi
        else
            if python3 tools/update-full-hash.py "$file"; then
                updated=$((updated + 1))
            else
                skipped=$((skipped + 1))
            fi
        fi
    done

    echo "   Totaal bestanden : $total"
    echo "   Updated / Would update : $updated"
    echo "   Skipped          : $skipped"
done

echo -e "\n=== KLAAR ==="