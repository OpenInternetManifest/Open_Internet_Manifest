# Guide – Nextcloud installeren (je eigen cloud)

Nextcloud is open-source software voor je eigen cloud: bestanden, foto’s, kalender, contacten – alles onder jouw controle.

**Tijd:** 30–60 minuten (eenmalig)  
**Kosten:** €0 (op bestaande hardware) of €50–€100 (kleine VPS)

### Optie 1 – Snelste start: Nextcloud op een Raspberry Pi (met Umbrel of YunoHost)
<details>
<summary>Je hebt al een Pi met Umbrel of YunoHost → klik hier</summary>

- In Umbrel: ga naar App Store → zoek "Nextcloud" → installeren met één klik
- In YunoHost: ga naar Apps → Nextcloud → installeren
- Wacht 5–10 minuten → klaar!
</details>

### Optie 2 – Nextcloud op een VPS (aanbevolen voor beginners)
<details>
<summary>Ik wil een kant-en-klare server</summary>

Goede providers (2025):
- <a href="https://www.hetzner.com/cloud" target="_blank">Hetzner Cloud</a> – €5/maand voor goede prestaties
- <a href="https://contabo.com" target="_blank">Contabo</a> – goedkoop en betrouwbaar
- <a href="https://www.ionos.nl" target="_blank">IONOS</a> – Nederlands, eenvoudige setup

Gebruik een “Nextcloud ready” image of installeer via snap (zie optie 3).
</details>

### Optie 3 – Handmatig op je eigen server (bijv. Intel NUC of VPS)
<details>
<summary>Volledige controle – stap-voor-stap</summary>

**Benodigdheden:**
- Ubuntu 24.04 LTS server (of Debian 12)
- Minimaal 2 GB RAM, 20 GB SSD
- Domeinnaam (optioneel, maar aanbevolen voor HTTPS)

**Stappen:**

1. Update het systeem
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Installeer benodigde pakketten (opgesplitst voor betere weergave)
    ```bash
   sudo apt install apache2 mariadb-server php php-mysql php-gd php-curl php-mbstring php-xml php-zip -y
    sudo apt install php-intl php-bcmath php-gmp unzip wget -y
    ```
3. Maak een database
    ```bash
    sudo mysql -u root -e "CREATE DATABASE nextcloud;"
    sudo mysql -u root -e "CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY 'sterkwachtwoord';"
    sudo mysql -u root -e "GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'localhost';"
    sudo mysql -u root -e "FLUSH PRIVILEGES;"
    ```
4. Download Nextcloud
      ```bash
    cd /var/www
    sudo wget https://download.nextcloud.com/server/releases/latest.zip
    sudo unzip latest.zip
    sudo mv nextcloud html
    sudo chown -R www-data:www-data html
    ```
5. Configureer Apache (virtuele host)
Maak /etc/apache2/sites-available/nextcloud.conf:
      ```bash
    <VirtualHost *:80>
    ServerName jouwdomein.nl
    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options +FollowSymlinks
        AllowOverride All
        Require all granted
    </Directory>
    </VirtualHost>
    ```
Activeer:
  ```bash
   sudo a2ensite nextcloud
   sudo a2enmod rewrite headers env dir mime ssl
   sudo systemctl restart apache2
   ```
6. HTTPS met Let's Encrypt (aanbevolen)
    ```bash
    sudo apt install certbot python3-certbot-apache -y
    sudo certbot --apache -d jouwdomein.nl
    ```
Voltooi installatie via browser
Open https://jouwdomein.nl → vul admin-gegevens en database-info in → klaar!

Je data synchroniserenTelefoon: Nextcloud app (Android/iOS)
Computer: Nextcloud desktop client


Je foto’s, documenten en herinneringen zijn nu echt van jou.<div style="text-align: center; margin-top: 2em; padding: 1em; background: #f0f0f0; border-radius: 8px;">

</details>   <!-- EINDE van optie 3 dropdown -->
      
---

<div style="text-align: center; margin-top: 2em; padding: 1em; background: #f0f0f0; border-radius: 8px;">
<strong>🗣️ Praat mee over Friendica</strong><br>
<a href="https://matrix.to/#/#openinternetmanifest:matrix.org?via=matrix.org">Open Element en praat mee</a><br>
<small>Kleine tip: typ "Guide NextCloud" als eerste bericht</small>

</div>

---

💸 <strong> Doneer anoniem in crypto<br>

| Cryptocurrency     | QR-code (klik om te vergroten)                                                                                                                                        | Adres (klik om te kopiëren)                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **Bitcoin (BTC)**  | ![Bitcoin QR](https://api.qrserver.com/v1/create-qr-code/?size=200x200&margin=20&data=bitcoin:bc1qn0wpgqc9g22hpcyeu8687tdv3gg83rnvksrydm)      | `bc1qn0wpgqc9g22hpcyeu8687tdv3gg83rnvksrydm`                     
| **Monero (XMR)**   | ![Monero QR](https://api.qrserver.com/v1/create-qr-code/?size=200x200&margin=20&data=monero:49o77fXDwS9fdtMqBABjrGVRe3evQ66tXQsb8dBWvFjxSsdaiiZppqGj59nXoD3ySeY13jmKUcji4JYGmj3v41fWFSys84F) | `85J34VDW5wSJG6yuWXyYzB4ScedX7k4FJZktSk1VMo2uRHFWoPjB9cXKGiEkvw1SvoQrMXdxwnrVPZVzJx9MrPe4HoPYbFu` |

**Monero-tip**: met Cake Wallet of de officiële GUI krijgt elke donateur automatisch een uniek subaddress → maximale privacy.

Heel erg bedankt voor je steun – jullie houden dit project in leven! 🚀

---

<div style="text-align: left; margin-top: 2em; padding: 1em; background: #f8f8f8; border-left: 4px solid #ccc; font-size: 0.9em;">

  ### Disclaimer
Alle guides worden door de community voorgesteld en door het OIM-coreteam gecontroleerd voordat ze live gaan.  
Toch blijft het uitvoeren van technische stappen jouw eigen verantwoordelijkheid.  
Het Open Internet Manifest is niet aansprakelijk voor schade, dataverlies of andere problemen die kunnen ontstaan door het volgen van een guide.
</div>

---

| [← Thesis 23](/Open_Internet_Manifest/NL/theses/thesis-23) | [← Alle theses →](/Open_Internet_Manifest/NL/manifest) | [← Alle guides →](/Open_Internet_Manifest/NL/guides) |
|---: <div style="text-align: center; margin: 3em 0 2em; font-size: 0.9em; color: #888;">
  ← <a href="javascript:history.back()"><div style="text-align: center; margin: 3em 0 2em; font-size: 0.9em; color: #888;">
  ← <a href="javascript:history.back()">Terug naar vorige pagina</a>
</div>
s page</a>
</div>

---: |


