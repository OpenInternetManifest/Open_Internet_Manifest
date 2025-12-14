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

Tip voor Intel NUC demo-server: Gebruik dezelfde stappen – NUC is krachtig genoeg voor tientallen gebruikers.</details>
```

