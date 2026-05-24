#!/bin/bash
# bulk-update-hashes.sh - Update ALL RVN posts

echo "=== Bulk hash update started ==="

find _social-posts/nl -name "day-*.md" | sort | while read file; do
    echo "Processing: $file"
    ./.github/scripts/calculate-hashes.sh "$file"
done

find _social-posts/en -name "day-*.md" | sort | while read file; do
    echo "Processing: $file"
    ./.github/scripts/calculate-hashes.sh "$file"
done

echo "=== Bulk update finished ==="
echo "Je kunt nu de site rebuilden met: bundle exec jekyll build"
