#!/bin/bash
# tools/fix-all-clean-text.sh - ALL files (incl teasers etc)

MODE=$1   # dry of update

echo "=== Clean Text Fixer (ALL .md files) ==="

for dir in nl en; do
    echo -e "\n→ Processing _social-posts/$dir ..."

    count_total=0
    count_fixed=0
    count_skipped=0

    for file in _social-posts/$dir/*.md; do
        [ -f "$file" ] || continue
        count_total=$((count_total + 1))
        
        if [ "$MODE" = "update" ]; then
            python3 tools/fix-clean-text.py "$file" --update
            if [ $? -eq 0 ]; then
                count_fixed=$((count_fixed + 1))
            else
                count_skipped=$((count_skipped + 1))
            fi
        else
            if python3 tools/fix-clean-text.py "$file"; then
                count_fixed=$((count_fixed + 1))
            else
                count_skipped=$((count_skipped + 1))
            fi
        fi
    done

    echo "   Totaal bestanden      : $count_total"
    if [ "$MODE" = "update" ]; then
        echo "   Gefixt                : $count_fixed"
    else
        echo "   Would fix             : $count_fixed"
    fi
    echo "   Al goed (skipped)     : $count_skipped"
done

echo -e "\n=== KLAAR ==="