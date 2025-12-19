import hashlib

theses = [
    "**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters",
    # ... voeg alle 10 toe
]

for i, text in enumerate(theses, 1):
    hash_obj = hashlib.sha256(text.encode('utf-8'))
    print(f"Thesis {i}: sha256: {hash_obj.hexdigest()}")





- ...

### English version (EN/manifest.md)
Idem voor EN.

Plus: vermeld de GitHub commit-hash voor extra context (bijv. "Gebaseerd op commit `abc123...`").

---

| [Start Pagina](/NL/index.md) | [About en steun OIM](/NL/over.md) |
---: | ---: |
