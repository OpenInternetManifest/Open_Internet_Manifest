# Hash System v2 – Fuzzy Only (April 2026)

**Status:** Definitief werkend  
**Datum:** 18 april 2026

We gebruiken nu alleen nog **fuzzy_sha256** voor alle verificatie (website + socials).

## Bestanden
- `debug-hashes-v41.sh` → lokale debug & testen
- `hash-verify-v41.js` → copy button + verifier op de site
- `calculate-hashes-v41.sh` → GitHub Action na merge
- `process-rvn-merge-v41.yml` → workflow

## Kenmerken
- Zeer robuuste fuzzy hash (alle witregels weg, markdown gestript, lowercase, spaties genormaliseerd)
- Copy button, debug tool en Action geven exact dezelfde tekst → dezelfde hash
- Werkt met tabellen (worden voor hashing platgeslagen)
- Giscus, footer en ongewenste elementen worden automatisch verwijderd

Dit is de versie die we vanaf nu als basis gebruiken.
