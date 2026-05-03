---
layout: guides
lang: nl
order: 9
title: "Node van buitenaf bereikbaar maken"
difficulty: gevorderd
teaser: "Je Umbrel-node draait lokaal. Hoe maak je hem veilig bereikbaar vanaf overal? Van simpel tot geavanceerd."
slug: node-bereikbaar-maken
---

# Node van buitenaf bereikbaar maken

Je Umbrel-node draait nu alleen lokaal (http://umbrel.local). Hoe bereik je hem veilig vanaf je telefoon of laptop als je niet thuis bent?

Hieronder de beste methodes, van eenvoudig naar geavanceerd.

### Overzicht methodes

| Methode                  | Moeilijkheid | Snelheid     | Privacy / Beveiliging | Beste voor                              | Tijd om op te zetten |
|--------------------------|--------------|--------------|-----------------------|-----------------------------------------|----------------------|
| **Tor Onion** (start)    | ★☆☆☆☆       | Traag        | Maximaal              | Maximale privacy, geen account          | 2 minuten           |
| **Tailscale HTTP**       | ★★☆☆☆       | Snel         | Hoog (WireGuard)      | Dagelijks gebruik, Nextcloud-sync       | 5–10 minuten        |
| **Tailscale HTTPS**      | ★★★★☆       | Snel         | Zeer hoog             | Apps die HTTPS eisen, groen slotje      | 15–30 minuten       |

**Aanbeveling:** Begin met Tor. Upgrade naar Tailscale als je snelheid en gemak wilt.

### Optie 1: Tor Onion – makkelijkste & meest private manier

**Waarom Tor?**  
Geen account, geen poorten openzetten, werkt overal.

**Stappen (2 minuten):**
1. Open Umbrel-dashboard (http://umbrel.local)
2. Ga naar Settings → Advanced Settings → Remote Access
3. Zet Tor aan
4. Kopieer de gegenereerde .onion-link

**Toegang:**
- Android: Tor Browser
- iPhone: Onion Browser of Orbot
- Laptop: Tor Browser (torproject.org)

Nextcloud gebruik je via http://jouw-onion-link/nextcloud in de Tor Browser.

### Optie 2: Tailscale HTTP – snel voor dagelijks gebruik

**Stappen:**
1. Umbrel App Store → zoek Tailscale → installeer
2. Open Tailscale → log in met Google/Apple/GitHub
3. Zet Tailscale aan op je node
4. Installeer Tailscale op je telefoon/laptop en log in met hetzelfde account
5. Kopieer de Magic DNS-naam (bijv. umbrel.abcdef123.ts.net)
6. Open in browser: http://umbrel.abcdef123.ts.net

Nextcloud: http://umbrel.abcdef123.ts.net/nextcloud

### Optie 3: Tailscale HTTPS – geavanceerd (groen slotje)

**Stappen:**
1. Installeer Tailscale (zie Optie 2)
2. Via Terminal in Umbrel: tailscale serve 8080 (of de juiste poort)
3. Configureer trusted domains in Nextcloud via occ-commando’s (zie onder)

**Veelgemaakte fouten & fixes:**
- "Access through untrusted domain" → voeg domein toe met:  
  sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set trusted_domains 1 --value="umbrel.abcdef123.ts.net"  
  sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set overwriteprotocol --value="https"  
  sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set overwrite.cli.url --value="https://umbrel.abcdef123.ts.net/nextcloud"

- Herstart container: sudo docker restart nextcloud_web_1

Je node is nu van buitenaf bereikbaar. Volgende stap: praktische toepassingen (Nextcloud-sync, Immich, wallets) en redundancy.

