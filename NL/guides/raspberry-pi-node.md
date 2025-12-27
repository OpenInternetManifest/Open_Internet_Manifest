# Guide – Je eigen sovereign node draaien (Raspberry Pi + Umbrel)

Dit is dé manier om je eigen stukje internet te bezitten: Bitcoin-node, Nostr-relay, Nextcloud, foto-backup, alles thuis, alles van jou.

**Totale eenmalige kosten:** € 180 – € 280  
**Maandkosten:** ± € 3 (stroom)

### Wat je nodig hebt (vergelijk prijzen via Tweakers – opent in nieuw tabblad)
<details>
<summary>Ik weet niet wat ik moet kopen → klik hier</summary>

- **Raspberry Pi 5 (8 GB)** → <a href="https://tweakers.net/pricewatch/1986384/raspberry-pi-5-8gb-ram.html" target="_blank">Vergelijk prijzen op Tweakers (€99,99 bij 46 winkels)</a>  
- **Of goedkoper: Raspberry Pi 4 (8 GB)** → <a href="https://tweakers.net/pricewatch/1562568/raspberry-pi-4-model-b-8gb-ram.html" target="_blank">Vergelijk prijzen op Tweakers (€89 bij 15 winkels)</a>  
- **Micro-SD-kaart 128 GB** → <a href="https://tweakers.net/pricewatch/450844/samsung-evo-plus-128gb-microsdxc-card-sd-adapter.html" target="_blank">Vergelijk prijzen op Tweakers (€12,50 bij 55 winkels)</a>  
- **Externe SSD 1 TB (aanrader!)** → <a href="https://tweakers.net/pricewatch/1807446/samsung-portable-ssd-t7-shield-1tb-zwart.html" target="_blank">Vergelijk prijzen op Tweakers (€137 bij 24 winkels)</a>  
- **Voeding + ethernetkabel** zitten meestal bij de starter-kit
</details>

### Stap 1 – Umbrel downloaden
<details>
<summary>Ik weet niet waar ik Umbrel vind</summary>
Ga naar <a href="https://github.com/getumbrel/umbrel/wiki/Install-umbrelOS-on-a-Raspberry-Pi-5#installing-umbrelos-on-the-nvme-or-usb-drive" target="_blank">umbrel</a> → Kies voor de juiste versie voor jouw Pi4, Pi5 of AMD64".
</details>

### Stap 2 – Image flashen met Balena Etcher
<details>
<summary>Ik heb nog nooit iets geflasht</summary>

1. Download Balena Etcher: <a href="https://etcher.balena.io" target="_blank">etcher.balena.io</a>  
2. Start Etcher  
3. Klik "Flash from file" → kies het gedownloade umbrel-bestand  
4. Klik "Select target" → kies je SD-kaart  
5. Klik "Flash!" → koffie halen (5-10 minuten)  
6. Etcher zegt "Flash Complete" → klaar!
</details>

### Stap 3 – Alles aansluiten
<details>
<summary>Hoe sluit ik de Pi aan?</summary>

1. SD-kaart in de Pi stoppen  
2. SSD via USB aansluiten (als je die hebt)  
3. Ethernetkabel in je router  
4. Voeding erin → Pi gaat vanzelf aan (lampjes gaan knipperen)
</details>

### Stap 4 – Umbrel opstarten
<details>
<summary>Hoe kom ik bij mijn Umbrel?</summary>

Open je browser en typ:  
http://umbrel.local  

(of zoek in je router-app naar een apparaat "umbrel")
</details>

### Stap 5 – Eerste setup
Wachtwoord kiezen → klaar!  
Je hebt nu thuis:
- Bitcoin + Lightning node  
- Nostr relay  
- Nextcloud (je eigen Dropbox)  
- PhotoPrism (je eigen Google Photos)  
- Mastodon-server (optioneel)  
- 40+ apps met één klik

### Wat als het niet werkt?
<details>
<summary>Ik zie geen umbrel.local</summary>

- Probeer http://[IP-adres van de Pi] (staat in je router)  
- Of sluit een scherm + toetsenbord aan en log in met gebruiker "umbrel", wachtwoord "moneyprintergobrrr"
</details>

Kosten per maand: ± € 3 elektriciteit  
Veiligheid: jij hebt de enige sleutel  
Niemand kan je ooit nog deactiveren

---

<div style="text-align: center; margin-top: 2em; padding: 1em; background: #f0f0f0; border-radius: 8px;">
<strong>🗣️ Praat mee over sovereign nodes</strong><br>
<a href="https://matrix.to/#/#openinternetmanifest:matrix.org?via=matrix.org">Open Element en praat mee</a><br>
<small>Kleine tip: typ "sovereign node" als eerste bericht</small>
</div>

---

### Ondersteun het Open Internet Manifest ❤️
Dit manifest blijft alleen bestaan dankzij jullie donaties.  
Elke satoshi of monero helpt enorm (servers, domeinen, ontwikkeling).

## 💸 Doneer anoniem in crypto

| Cryptocurrency     | QR-code (klik om te vergroten)                                                                                                                                        | Adres (klik om te kopiëren)                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **Bitcoin (BTC)**  | [![Bitcoin QR](https://api.qrserver.com/v1/create-qr-code/?size=150x150&margin=20&data=bitcoin:bc1qn0wpgqc9g22hpcyeu8687tdv3gg83rnvksrydm)](https://api.qrserver.com/v1/create-qr-code/?size=600x600&data=bitcoin:bc1qn0wpgqc9g22hpcyeu8687tdv3gg83rnvksrydm)      | `bc1qn0wpgqc9g22hpcyeu8687tdv3gg83rnvksrydm`                     
| **Monero (XMR)**   | [![Monero QR](https://api.qrserver.com/v1/create-qr-code/?size=150x150&margin=20&data=monero:49o77fXDwS9fdtMqBABjrGVRe3evQ66tXQsb8dBWvFjxSsdaiiZppqGj59nXoD3ySeY13jmKUcji4JYGmj3v41fWFSys84F)](https://api.qrserver.com/v1/create-qr-code/?size=600x600&data=monero:49o77fXDwS9fdtMqBABjrGVRe3evQ66tXQsb8dBWvFjxSsdaiiZppqGj59nXoD3ySeY13jmKUcji4JYGmj3v41fWFSys84F) | `85J34VDW5wSJG6yuWXyYzB4ScedX7k4FJZktSk1VMo2uRHFWoPjB9cXKGiEkvw1SvoQrMXdxwnrVPZVzJx9MrPe4HoPYbFu` |

**Monero-tip**: met Cake Wallet of de officiële GUI krijgt elke donateur automatisch een uniek subaddress → maximale privacy.

Heel erg bedankt voor je steun – jullie houden dit project in leven! 🚀

---


  ### Disclaimer
Alle guides worden door de community voorgesteld en door het OIM-coreteam gecontroleerd voordat ze live gaan.  
Toch blijft het uitvoeren van technische stappen jouw eigen verantwoordelijkheid.  
Het Open Internet Manifest is niet aansprakelijk voor schade, dataverlies of andere problemen die kunnen ontstaan door het volgen van een guide.
</div>

---

