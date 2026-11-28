#!/bin/bash
# scripts/clean_backups.sh – verwijder alle .backup* files veilig

echo "Zoeken naar backup-files..."

# Dry-run eerst: toon wat er verwijderd zou worden
find . -type f -name "*.backup*" -print

echo ""
read -p "Wil je deze bestanden echt verwijderen? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
  find . -type f -name "*.backup*" -delete
  echo "Alle .backup* files verwijderd!"
  echo "Commit dit met: git add . && git commit -m 'cleanup all backup files after migration'"
else
  echo "Geen bestanden verwijderd."
fi