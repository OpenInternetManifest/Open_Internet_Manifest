---
layout: default
title: Cryptografische hash
lang: nl
permalink: /nl/begrippen/cryptografische-hash/
---

Een **cryptografische hash** is een wiskundige functie die elke willekeurige hoeveelheid data (zoals een tekst, bestand of thesis) omzet in een vaste lengte unieke "vingerafdruk" (bij dit manifest: 64 tekens in SHA-256).

**Belangrijke eigenschappen:**
- **Uniek**: zelfs één spatie of punt verschil geeft een volledig andere hash.
- **Onomkeerbaar**: je kunt nooit de originele tekst reconstrueren uit de hash.
- **Voorspelbaar**: dezelfde tekst geeft altijd exact dezelfde hash.
- **Snel**: een hele thesis hashen kost milliseconden.

**Waarom gebruiken wij hashes in het Open Internet Manifest?**
- Elke thesis, guide en begrip heeft een officiële hash.
- Jij als lezer kunt de tekst kopiëren, zelf hashen (met SHA-256), en vergelijken met de officiële hash.
- Matcht het? Dan weet je 100% zeker dat je de authentieke, onveranderde versie leest.
- Wijzigt iemand (zelfs de beheerder) één letter? Dan klopt de hash niet meer → wijziging direct zichtbaar.

De hashes maken het manifest **decentraal verifieerbaar**: geen vertrouwen nodig in een centrale bron, alleen in wiskunde.

> "Een hash is digitaal zegelwas: breek je het, dan ziet iedereen het."  
> — Ruben Berkhout