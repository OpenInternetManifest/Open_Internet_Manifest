import hashlib

theses = [
    "**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters",
    "**Thesis 2** — Zij die het open internet hebben ingesloten verkopen je nu het verhaal dat echte vrijheid iets uit de jaren tachtig was",
    "**Thesis 3** — In de echte wereld zou niemand accepteren wat wij online al jaren slikken",
    "**Thesis 4** — De omheiningen zijn bijna voltooid, maar het laatste hek staat nog open",
    "**Thesis 5** — Alleen een echt open internet geeft echte digitale vrijheid",
    "**Thesis 6** — Exit zonder bouwen is vluchten; bouwen zonder exit is collaboreren",
    "**Thesis 7** — Een open internet geeft privacy zijn oude kracht terug",
    "**Thesis 8** — Een open internet bevrijdt je stem en je creativiteit van willekeur",
    "**Thesis 9** — Een open internet maakt echte economische vrijheid weer mogelijk",
    "**Thesis 10** — Het digitale hok breidt zich uit naar de echte wereld"
]

for i, text in enumerate(theses, 1):
    hash_obj = hashlib.sha256(text.encode('utf-8'))
    print(f"- Thesis {i}: sha256: {hash_obj.hexdigest()}")

