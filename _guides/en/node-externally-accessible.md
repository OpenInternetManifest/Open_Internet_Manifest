---
layout: guides
lang: en
order: 9
title: "Make your node accessible from outside"
difficulty: advanced
teaser: "Your Umbrel node is now only accessible locally. How do you reach it safely from anywhere in the world? From simple to advanced."
slug: node-remote-access
---

# Make your node accessible from outside

Your Umbrel node now only runs locally (`http://umbrel.local`). How do you reach it safely from your phone or laptop when you're not at home?

Below are the best methods, from simple to advanced.

### Overview of methods

| Method                   | Difficulty   | Speed        | Privacy / Security    | Best for                                | Setup time          |
|--------------------------|--------------|--------------|-----------------------|-----------------------------------------|---------------------|
| **Tor Onion** (start)    | ★☆☆☆☆       | Slow         | Maximum               | Maximum privacy, no account             | 2 minutes           |
| **Tailscale HTTP**       | ★★☆☆☆       | Fast         | High (WireGuard)      | Daily use, Nextcloud sync               | 5–10 minutes        |
| **Tailscale HTTPS**      | ★★★★☆       | Fast         | Very high             | Apps that require HTTPS, green padlock  | 15–30 minutes       |

**Recommendation:** Start with **Tor**. Upgrade to Tailscale when you want speed and convenience.

### Option 1: Tor Onion – easiest & most private method

**Why Tor?**  
No account, no port forwarding, works everywhere.

**Steps (2 minutes):**
1. Open Umbrel dashboard (`http://umbrel.local`)
2. Go to **Settings → Advanced Settings → Remote Access**
3. Enable **Tor**
4. Copy the generated `.onion` link

**Access:**
- **Android:** Tor Browser
- **iPhone:** Onion Browser or Orbot
- **Laptop:** Tor Browser (torproject.org)

Nextcloud: `http://your-onion-link/nextcloud` (in Tor Browser).

### Option 2: Tailscale HTTP – fast for daily use

**Steps:**
1. Umbrel App Store → search **Tailscale** → install
2. Open Tailscale → log in with Google/Apple/GitHub
3. Enable Tailscale on your node
4. Install Tailscale on your phone/laptop and log in with the same account
5. Copy the **Magic DNS name** (e.g. `umbrel.abcdef123.ts.net`)
6. Open in browser: `http://umbrel.abcdef123.ts.net`

Nextcloud: `http://umbrel.abcdef123.ts.net/nextcloud`

### Option 3: Tailscale HTTPS – green padlock (advanced)

**Steps:**
1. Install Tailscale (see Option 2)
2. In Umbrel Terminal: `tailscale serve 8080` (or correct port)
3. Configure trusted domains in Nextcloud via occ commands (see below)

**Common errors & fixes:**
- "Access through untrusted domain" → add domain with:  
  `sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set trusted_domains 1 --value="umbrel.abcdef123.ts.net"`  
  `sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set overwriteprotocol --value="https"`  
  `sudo docker exec --user www-data nextcloud_web_1 php occ config:system:set overwrite.cli.url --value="https://umbrel.abcdef123.ts.net/nextcloud"`

- Restart container: `sudo docker restart nextcloud_web_1`

Your node is now accessible from anywhere. Next step: practical applications (Nextcloud sync, Immich, wallets) and redundancy.
