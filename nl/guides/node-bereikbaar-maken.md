---
layout: default
lang: nl
order: 9
title: " Node van buitenaf bereikbaar maken – kies de methode die bij jou past"
difficulty: gevorderd      # of: gemiddeld / gevorderd
teaser: "Je Umbrel-node draait nu lokaal (http://umbrel.local), maar hoe bereik je 'm veilig vanaf je telefoon of laptop als je niet thuis bent? Er zijn meerdere manieren, van super simpel tot geavanceerd. We raden aan te beginnen met de makkelijkste."
slug: element-migratie
---
# Node van buitenaf bereikbaar maken – kies de methode die bij jou past

Je Umbrel-node draait nu lokaal (http://umbrel.local), maar hoe bereik je 'm veilig vanaf je telefoon of laptop als je niet thuis bent? Er zijn meerdere manieren, van super simpel tot geavanceerd. We raden aan te beginnen met de makkelijkste.

### Welke methode kies jij?

| Methode                          | Moeilijkheid | Snelheid | Privacy/Security | Wanneer kiezen?                              | Tijd om op te zetten | Platform-opmerkingen                  |
|----------------------------------|--------------|----------|------------------|----------------------------------------------|----------------------|---------------------------------------|
| **Tor Onion** (aanbevolen start) | ★☆☆☆☆       | Traag    | Maximaal         | Maximale privacy, geen extra account         | 2 minuten           | Android goed, iPhone traag (Orbot)   |
| **Tailscale HTTP**               | ★★☆☆☆       | Snel     | Hoog (WireGuard) | Dagelijks gebruik, filesync vanaf telefoon   | 5-10 minuten        | Werkt op alle apparaten               |
| **Tailscale HTTPS**              | ★★★★☆       | Snel     | Zeer hoog        | Groen slotje, apps die HTTPS eisen           | 15-30 minuten       | Vereist terminal (zie geavanceerd)    |
| Andere (Zerotier, Headscale, etc.) | ★★★★★     | Variabel | Hoog             | Geen Tailscale-account                       | 30+ minuten         | Voor hardcore decentralisten          |

**Waarom Tor als start?** Geen gedoe met accounts of poorten openzetten.  
**Waarom Tailscale als upgrade?** Veel sneller voor Nextcloud-sync, foto's uploaden etc.

### Optie 1: Tor Onion – de makkelijkste & meest private manier

**Waarom?**  
Geen extra installaties, geen account, geen poorten open → maximale privacy. Werkt overal (achter CG-NAT, carrier NAT).  
Nadelen: traag voor grote bestanden (foto's, video's).

**Stappen (2 minuten):**

1. Open Umbrel-dashboard (http://umbrel.local).
2. Ga naar **Instellingen** → **Geavanceerde instellingen** → **Toegang op afstand**.
3. Zet **Via Tor** aan.
4. Umbrel genereert een .onion-link (bijv. http://lange-string.onion).
5. Kopieer de link en bewaar veilig.

**Toegang vanaf je apparaat:**

- **Android:** Installeer Tor Browser (Play Store) → plak .onion-link → dashboard opent.
- **iPhone:** Installeer Onion Browser of Orbot (App Store). **Let op:** Orbot laadt vaak traag of is instabiel op iOS. Probeer Onion Browser als alternatief.
- **Laptop/PC:** Tor Browser downloaden (torproject.org) → plak link.

Voor Nextcloud: http://[jouw-onion]/nextcloud (gebruik Tor Browser).  
Voor mobiele Nextcloud-app: Tor niet direct ondersteund → gebruik webversie in Tor Browser.

**Screenshot:** [Umbrel: Toegang op afstand → Tor toggle + .onion link]

**Tip:** Bookmark de .onion-link in Tor Browser. Test eerst op laptop als het traag voelt op telefoon.

### Optie 2: Tailscale HTTP – sneller voor dagelijks gebruik (geen terminal nodig)

**Waarom?**  
Snel (WireGuard), mooie link (umbrel.jouwtailnet.ts.net), veilig end-to-end encrypted. Geen poorten open.

**Stappen:**

1. Umbrel App Store → zoek "Tailscale" → Install.
2. Open Tailscale app → Authenticate → log in met Google/Apple/GitHub (gratis account).
3. Toggle VPN aan.
4. Op telefoon/laptop: login.tailscale.com → log in met hetzelfde account → zie je "umbrel" node.
5. Klik op de node → copy **Magic DNS name** (bijv. umbrel.tai123456.ts.net).
6. Open browser → **http://"naam server"."tail123456".ts.net** (zonder https!).
7. Dashboard laadt → Nextcloud op http://.../nextcloud.

**Mobiel:**
- Installeer Tailscale app (iOS/Android) → login → auto-connect.
- Nextcloud app: server = http://http://"naam server"."....".ts.net/nextcloud.

**Screenshot:** [Tailscale admin → Magic DNS naam]

**Waarschuwing:** Sommige apps eisen HTTPS → kies dan Optie 3 of blijf bij Tor.

### Optie 3: Tailscale HTTPS – geavanceerd (groen slotje)

**Waarschuwing:** Dit vereist terminal-commando's. Niet voor beginners. HTTP is vaak genoeg (veilig via Tailscale).

**Stappen:**

1. Umbrel App Store → Tailscale install & authenticate (zoals Optie 2).
2. Settings → Advanced → Terminal → selecteer App: Tailscale.
3. Run: `tailscale serve 8080` (of 8081 als Umbrel op 8081 draait – check met netstat in hoofdterminal).
4. Check: `tailscale serve status` → zie proxy naar 127.0.0.1:8080.
5. Test: https://"naam server"."tail123456".ts.net (moet nu met groen slot laden).

**Persistent maken (optioneel):** Run in screen of maak startup script via Portainer.

**Veelgemaakte fouten & fixes:**
- Permission denied op docker? Gebruik sudo: `sudo docker ps | grep nextcloud` → container-naam is vaak nextcloud_web_1.
- "Access through untrusted domain"? Fix trusted_domains:

 1. sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set trusted_domains 1 --value="umbrel.tail63975b.ts.net"
 2. sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set overwriteprotocol --value="https"
 3. sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set overwrite.cli.url --value="https://umbrel.tail63975b.ts.net/nextcloud"
 4. sudo docker restart nextcloud_web_1

 - Foute entries in trusted_domains (bijv. met :8081 of dubbele ts.net)? Verwijder:

   sudo docker exec --user www-data nextcloud_web_1 php occ config:system:delete trusted_domains [index]

Check met `... get trusted_domains`.

**Screenshot:** [tailscale serve status, trusted_domains lijst, login-scherm mobiel]

Zodra dit werkt → ga naar de volgende guide: Praktische toepassingen (Nextcloud sync, wallets, Immich) en redundancy (Syncthing mirror).



