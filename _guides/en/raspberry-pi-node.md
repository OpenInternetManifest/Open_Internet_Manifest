---
layout: guides
lang: en
order: 11
title: "Run your own sovereign node at home (Raspberry Pi + Umbrel)"
difficulty: medium
teaser: "This is the way to own your own piece of the internet: Bitcoin node, Lightning, Nostr, Nextcloud, photo backup – all at home, all yours."
slug: sovereign-node
---

# Run your own sovereign node at home (Raspberry Pi + Umbrel)

This is one of the most powerful steps you can take: running your own **sovereign node** at home. A complete, independent server under your full control.

**Hardware choice (2026):**
- **Raspberry Pi 5 (8 GB)** → Best for beginners.
- **Refurbished Mini-PC (i5/i7)** → Often similar price but more powerful (good if no AI planned).
- **Powerful Mini-PC (Ryzen 7 8845HS or higher, 32 GB RAM)** → Recommended if you want to run your own local AI model later.

This guide focuses on the **Raspberry Pi 5**. A separate guide for Mini-PC setups is coming.

**One-time cost (Pi setup):** €180 – €280 (or equivalent)  
**Monthly cost:** ≈ €3 (electricity)

### What you need (Pi setup)

Hardware recommendations + price comparison

- **Raspberry Pi 5 (8 GB)** → [Search on Amazon](https://www.amazon.com/s?k=raspberry+pi+5+8gb) 
- **Micro-SD card 128 GB** → [Search on Amazon](https://www.amazon.com/s?k=micro+sd+128gb)
- **External SSD 1 TB (recommended!)** → [Search Samsung T7 Shield 1TB on Amazon](https://www.amazon.com/s?k=samsung+t7+shield+1tb)
- **Power supply + Ethernet cable (usually included in starter kits)**


### Step 1 – Download UmbrelOS

Go to the [Umbrel installation page](https://github.com/getumbrel/umbrel/wiki/Install-umbrelOS-on-a-Raspberry-Pi-5) and choose the correct version for your Pi.

### Step 2 – Flash the image with Balena Etcher

1. Download [Balena Etcher](https://etcher.balena.io)
2. Select the UmbrelOS file
3. Select your SD card
4. Click **Flash!**

### Step 3 – Connect the hardware

1. Insert SD card into the Pi
2. Connect SSD via USB (if you have one)
3. Plug Ethernet cable into your router
4. Plug in power → Pi starts automatically

### Step 4 – Start Umbrel

Open your browser and go to:  
**http://umbrel.local**

### Step 5 – First setup

Choose a strong password → your node is live!

You now have direct access to:
- Bitcoin + Lightning node
- Nostr relay
- Nextcloud (your own Dropbox)
- PhotoPrism (your own Google Photos)
- Many other apps with one click
