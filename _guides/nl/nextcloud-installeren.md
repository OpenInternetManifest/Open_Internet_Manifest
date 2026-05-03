---
layout: guides
lang: nl
order: 8
title: "Nextcloud installeren (je eigen cloud)"
difficulty: gemiddeld
teaser: "Nextcloud is open-source software voor je eigen cloud: bestanden, foto’s, kalender, contacten – alles onder jouw controle."
slug: nextcloud-installeren
---

# Nextcloud installeren (je eigen cloud)

Nextcloud is open-source software voor je eigen persoonlijke cloud. Bestanden, foto’s, agenda, contacten en meer — volledig onder jouw controle.

**Tijd:** 30–60 minuten (eenmalig)  
**Kosten:** €0 (op bestaande hardware) of €50–€100 (kleine VPS)

### Optie 1 – Snelste start: Nextcloud op een Raspberry Pi

Je hebt al een Pi met Umbrel of YunoHost?  
→ Ga naar de App Store (Umbrel) of Apps (YunoHost) → zoek "Nextcloud" → installeer met één klik. Wacht 5–10 minuten.

### Optie 2 – Nextcloud op een VPS (aanbevolen voor beginners)

Goede providers (2026):
- [Hetzner Cloud](https://www.hetzner.com/cloud) – vanaf €5/maand
- [Contabo](https://contabo.com) – goedkoop en krachtig
- [IONOS](https://www.ionos.nl) – Nederlands

Kies een “Nextcloud ready” image of installeer via Snap.

### Optie 3 – Handmatig installeren (volledige controle)

**Benodigdheden:** Ubuntu 24.04, minimaal 2 GB RAM, domeinnaam aanbevolen.

1. Update het systeem  
   `sudo apt update && sudo apt upgrade -y`

2. Installeer pakketten  
   `sudo apt install apache2 mariadb-server php php-mysql php-gd php-curl php-mbstring php-xml php-zip php-intl php-bcmath php-gmp unzip wget -y`

3. Maak database  
   `sudo mysql -u root -e "CREATE DATABASE nextcloud;"`  
   `sudo mysql -u root -e "CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY 'sterkwachtwoord';"`  
   `sudo mysql -u root -e "GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'localhost';"`  
   `sudo mysql -u root -e "FLUSH PRIVILEGES;"`

4. Download Nextcloud  
   `cd /var/www`  
   `sudo wget https://download.nextcloud.com/server/releases/latest.zip`  
   `sudo unzip latest.zip`  
   `sudo mv nextcloud html`  
   `sudo chown -R www-data:www-data html`

5. Configureer Apache + HTTPS  
   Volg de standaard Apache + Let's Encrypt handleiding en voltooi de installatie in de browser.

### Na installatie

- **Mobiel:** Nextcloud app (Android/iOS)  
- **Desktop:** Nextcloud Desktop Client

Je foto’s, documenten en herinneringen zijn nu écht van jou.

