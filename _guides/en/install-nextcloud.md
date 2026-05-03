---
layout: guides
lang: en
order: 8
title: "Install Nextcloud (your own cloud)"
difficulty: medium
teaser: "Nextcloud is open-source software for your personal cloud: files, photos, calendar, contacts — everything under your control."
slug: nextcloud-install
---

# Install Nextcloud (your own cloud)

Nextcloud is open-source software for your personal cloud. Files, photos, calendar, contacts and more — fully under your control.

**Time:** 30–60 minutes (one-time)  
**Cost:** €0 (on existing hardware) or €50–€100 (small VPS)

### Option 1 – Fastest start: Nextcloud on a Raspberry Pi

You already have a Pi with Umbrel or YunoHost?  
→ Go to the App Store (Umbrel) or Apps (YunoHost) → search for "Nextcloud" → install with one click. Wait 5–10 minutes.

### Option 2 – Nextcloud on a VPS (recommended for beginners)

Good providers (2026):
- [Hetzner Cloud](https://www.hetzner.com/cloud) – from €5/month
- [Contabo](https://contabo.com) – cheap and powerful
- [IONOS](https://www.ionos.com) – German, easy interface

Choose a “Nextcloud ready” image or install via Snap.

### Option 3 – Manual installation (full control)

**Requirements:** Ubuntu 24.04, at least 2 GB RAM, domain name recommended.

1. Update the system  
   `sudo apt update && sudo apt upgrade -y`

2. Install packages  
   `sudo apt install apache2 mariadb-server php php-mysql php-gd php-curl php-mbstring php-xml php-zip php-intl php-bcmath php-gmp unzip wget -y`

3. Create database  
   `sudo mysql -u root -e "CREATE DATABASE nextcloud;"`  
   `sudo mysql -u root -e "CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY 'strongpassword';"`  
   `sudo mysql -u root -e "GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'localhost';"`  
   `sudo mysql -u root -e "FLUSH PRIVILEGES;"`

4. Download Nextcloud  
   `cd /var/www`  
   `sudo wget https://download.nextcloud.com/server/releases/latest.zip`  
   `sudo unzip latest.zip`  
   `sudo mv nextcloud html`  
   `sudo chown -R www-data:www-data html`

5. Configure Apache + HTTPS  
   Follow the standard Apache + Let's Encrypt guide and complete the installation in the browser.

### After installation

- **Mobile:** Nextcloud app (Android/iOS)  
- **Desktop:** Nextcloud Desktop Client

Your photos, documents and memories are now truly yours.

