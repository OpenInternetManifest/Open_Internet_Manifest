# Trin 25 – Kør din egen node derhjemme (Raspberry Pi + Umbrel)

Dette er den ultimative måde at eje dit eget stykke internet på: Bitcoin-node, Nostr-relay, Nextcloud, foto-backup – alt hjemme, alt dit eget.

**Totale engangsomkostninger:** 1.300 – 2.000 kr.  
**Månedlige omkostninger:** ca. 20 kr. (strøm)

### Hvad du har brug for (sammenlign priser via PriceRunner – åbner i nyt faneblad)
<details>
<summary>Jeg ved ikke, hvad jeg skal købe → klik her</summary>

- **Raspberry Pi 5 (8 GB)** → <a href="https://www.pricerunner.dk/pl/10012-3208761544/Single-board-computere/Raspberry-Pi-5-8GB-Sammenlign-Priser" target="_blank">Sammenlign priser på PriceRunner (fra 709 kr. hos 2 butikker)</a> (eller søg på PriceRunner: <a href="https://www.pricerunner.dk/search?q=raspberry+pi+5+8gb" target="_blank">søg Raspberry Pi 5 8GB</a>)  
- **Eller billigere: Raspberry Pi 4 (8 GB)** → <a href="https://www.pricerunner.dk/pl/223-5211427/Stationaere-Computere/Raspberry-Pi-4-Model-B-8GB-Sammenlign-Priser" target="_blank">Sammenlign priser på PriceRunner (fra 675 kr. hos 15 butikker)</a> (eller søg på PriceRunner: <a href="https://www.pricerunner.dk/search?q=raspberry+pi+4+8gb" target="_blank">søg Raspberry Pi 4 8GB</a>)  
- **Micro-SD-kort 128 GB** → <a href="https://www.pricerunner.dk/sp/micro-sd-128gb.html" target="_blank">Sammenlign priser på PriceRunner (fra 54 kr. hos 88 butikker)</a> (eller søg på PriceRunner: <a href="https://www.pricerunner.dk/search?q=micro+sd+128gb" target="_blank">søg Micro-SD 128GB</a>)  
- **Ekstern SSD 1 TB (anbefalet! – hurtig, robust og stødsikker til dine data)** → <a href="https://www.pricerunner.dk/pl/36-3201275239/Harddiske/Samsung-Portable-SSD-T7-Shield-USB-3.2-1TB-Sammenlign-Priser" target="_blank">Sammenlign priser på PriceRunner (fra 749 kr. hos 27 butikker)</a> (eller søg på PriceRunner: <a href="https://www.pricerunner.dk/search?q=samsung+t7+shield+1tb" target="_blank">søg Samsung T7 Shield 1TB</a>)  
- **Strømforsyning + ethernetkabel** følger ofte med starter-kit'et
</details>

### Trin 1 – Download Umbrel
<details>
<summary>Jeg ved ikke, hvor jeg finder Umbrel</summary>
Gå til <a href="https://umbrel.com" target="_blank">umbrel.com</a> → klik på den store blå knap "Download Umbrel OS" (eller "Learn more" for instruktioner).
</details>

### Trin 2 – Flash image med Balena Etcher
<details>
<summary>Jeg har aldrig flashet noget før</summary>

1. Download Balena Etcher: <a href="https://etcher.balena.io" target="_blank">etcher.balena.io</a>  
2. Start Etcher  
3. Klik "Flash from file" → vælg det downloadede umbrel-fil  
4. Klik "Select target" → vælg dit SD-kort  
5. Klik "Flash!" → hent en kaffe (5-10 minutter)  
6. Etcher siger "Flash Complete" → færdig!
</details>

### Trin 3 – Tilslut alt
<details>
<summary>Hvordan tilslutter jeg Pi'en?</summary>

1. Sæt SD-kortet i Pi'en  
2. Tilslut SSD via USB (hvis du har en)  
3. Sæt ethernetkabel i din router  
4. Sæt strømmen i → Pi starter automatisk (lamperne blinker)
</details>

### Trin 4 – Start Umbrel op
<details>
<summary>Hvordan kommer jeg til min Umbrel?</summary>

Åbn din browser og skriv:  
http://umbrel.local  

(eller søg i din router-app efter et enhed "umbrel")
</details>

### Trin 5 – Første opsætning
Vælg et password → færdig!  
Du har nu derhjemme:
- Bitcoin + Lightning node  
- Nostr relay  
- Nextcloud (din egen Dropbox)  
- PhotoPrism (din egen Google Photos)  
- Mastodon-server (valgfri)  
- 40+ apps med ét klik

### Hvad hvis det ikke virker?
<details>
<summary>Jeg ser ikke umbrel.local</summary>

- Prøv http://[IP-adresse for Pi'en] (står i din router)  
- Eller tilslut en skærm + tastatur og log ind med bruger "umbrel", password "moneyprintergobrrr"
</details>

Omkostninger per måned: ca. 20 kr. strøm  
Sikkerhed: du har den eneste nøgle  
Ingen kan nogensinde deaktivere dig

← [Tilbage til Thesis 25](/DK/theses/thesis-25.md)
