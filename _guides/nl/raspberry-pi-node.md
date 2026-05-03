---
layout: guides
lang: nl
order: 11
title: "Je eigen sovereign node draaien"
difficulty: gemiddeld
teaser: "Dit is dé manier om je eigen stukje internet te bezitten: Bitcoin-node, Lightning, Nostr, Nextcloud, foto-backup — alles thuis en volledig van jou."
slug: sovereign-node
---

# Je eigen sovereign node draaien

Dit is een van de krachtigste stappen die je kunt zetten: je eigen **sovereign node** thuis draaien. Een complete, onafhankelijke server onder jouw controle.

### Hardware-keuze (2026)

- **Raspberry Pi 5 (8 GB)** → Beste keuze voor beginners. Laag verbruik, stil, goedkoop.
- **Refurbished Mini-PC (i5/i7)** → Vaak dezelfde prijs als een Pi, maar krachtiger en stiller. Goed als je geen AI wilt draaien.
- **Krachtige Mini-PC (Ryzen 7 8845HS of hoger, 32 GB RAM)** → Aanbevolen als je later een **eigen AI-model** (LLM) lokaal wilt draaien.

We focussen in deze guide op de **Raspberry Pi 5**, omdat die het meest toegankelijk is. Voor Mini-PC setups komt een aparte, uitgebreide guide.

**Totale eenmalige kosten (Pi-setup):** € 180 – € 280  
**Maandkosten:** ± € 3 (elektriciteit)

### Wat je nodig hebt (Pi-setup)

<details>
<summary>Hardware-aanbevelingen + prijsvergelijking (Tweakers)</summary>

- **Raspberry Pi 5 (8 GB)** → [Prijsvergelijking Tweakers](https://tweakers.net/pricewatch/1986384/raspberry-pi-5-8gb-ram.html)
- **Micro-SD-kaart 128 GB** → [Prijsvergelijking Tweakers](https://tweakers.net/pricewatch/450844/samsung-evo-plus-128gb-microsdxc-card-sd-adapter.html)
- **Externe SSD 1 TB** (sterk aanbevolen) → [Prijsvergelijking Tweakers](https://tweakers.net/pricewatch/1807446/samsung-portable-ssd-t7-shield-1tb-zwart.html)
- Voeding + ethernetkabel

</details>

### Stap 1 – UmbrelOS downloaden

Ga naar de [Umbrel installatiepagina](https://github.com/getumbrel/umbrel/wiki/Install-umbrelOS-on-a-Raspberry-Pi-5) en kies de juiste versie voor jouw Pi.

### Stap 2 – Image flashen met Balena Etcher

1. Download [Balena Etcher](https://etcher.balena.io)
2. Selecteer het UmbrelOS-bestand
3. Selecteer je SD-kaart
4. Klik op **Flash!**

### Stap 3 – Hardware aansluiten

1. SD-kaart in de Pi
2. SSD via USB aansluiten (als je die hebt)
3. Ethernetkabel in je router
4. Voeding aansluiten → Pi start automatisch op

### Stap 4 – Umbrel opstarten

Open in je browser: **http://umbrel.local**

### Stap 5 – Eerste setup

Kies een sterk wachtwoord → je node is live!

Je hebt nu direct toegang tot:
- Bitcoin + Lightning node
- Nostr relay
- Nextcloud (eigen cloud)
- PhotoPrism (eigen Google Photos)
- Veel andere apps met één klik

