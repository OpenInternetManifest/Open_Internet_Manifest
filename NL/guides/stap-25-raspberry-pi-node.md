# Stap 25 – Je eigen internet-node thuis draaien (Raspberry Pi + Umbrel)

Dit is dé manier om je eigen stukje internet te bezitten: Bitcoin-node, Nostr-relay, Nextcloud, foto-backup, alles thuis, alles van jou.

**Totale eenmalige kosten:** € 180 – € 280  
**Maandkosten:** ± € 3 (stroom)

### Wat je nodig hebt (klikbare Nederlandse shops)
<details>
<summary>Ik weet niet wat ik moet kopen → klik hier</summary>

- **Raspberry Pi 5 (8 GB) starter-kit** → https://www.kiwi-electronics.nl/raspberry-pi-5-8gb (of zoek op Kiwi: https://www.kiwi-electronics.nl/search?type=product&q=raspberry+pi+5)  
- **Of goedkoper: Raspberry Pi 4 (8 GB)** → https://www.coolblue.nl/product/917042/raspberry-pi-4-model-b-8gb.html (of zoek op Coolblue: https://www.coolblue.nl/zoeken?query=raspberry+pi+4+8gb)  
- **Micro-SD-kaart 128 GB** → https://www.coolblue.nl/product/906490/samsung-pro-plus-micro-sd-128gb.html (of zoek op Coolblue: https://www.coolblue.nl/zoeken?query=micro+sd+128gb)  
- **Externe SSD 1 TB (aanrader! – snel, robuust en schokbestendig voor je data)** → https://www.coolblue.nl/product/904675/samsung-t7-shield-1tb-zwart.html (of zoek op Coolblue: https://www.coolblue.nl/zoeken?query=samsung+t7+shield)  
- **Voeding + ethernetkabel** zitten meestal bij de starter-kit
</details>

### Stap 1 – Umbrel downloaden
<details>
<summary>Ik weet niet waar ik Umbrel vind</summary>
Ga naar https://umbrel.com → klik op de grote blauwe knop "Download Umbrel OS" (of "Learn more" voor instructies).
</details>

### Stap 2 – Image flashen met Balena Etcher
<details>
<summary>Ik heb nog nooit iets geflasht</summary>

1. Download Balena Etcher: https://etcher.balena.io  
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

← [Terug naar Thesis 25](/NL/theses/thesis-25.md)
