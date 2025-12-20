# Guide – Run your own sovereign node at home (Raspberry Pi + Umbrel)

This is the way to own your own piece of the internet: Bitcoin node, Nostr relay, Nextcloud, photo backup – all at home, all yours.

**One-time cost:** €180 – €280 (or equivalent in your currency)  
**Monthly cost:** ≈ €3 (electricity)

### What you need (compare prices on Amazon, AliExpress or local stores)
<details>
<summary>I don't know what to buy → click here</summary>

- **Raspberry Pi 5 (8 GB)** → <a href="https://www.amazon.com/s?k=raspberry+pi+5+8gb" target="_blank">Search on Amazon</a> or <a href="https://www.aliexpress.com/w/wholesale-raspberry-pi-5-8gb.html" target="_blank">AliExpress</a>  
- **Cheaper alternative: Raspberry Pi 4 (8 GB)** → <a href="https://www.amazon.com/s?k=raspberry+pi+4+8gb" target="_blank">Search on Amazon</a>  
- **Micro-SD card 128 GB** → <a href="https://www.amazon.com/s?k=micro+sd+128gb" target="_blank">Search on Amazon</a>  
- **External SSD 1 TB (recommended!)** → <a href="https://www.amazon.com/s?k=samsung+t7+shield+1tb" target="_blank">Search Samsung T7 Shield 1TB on Amazon</a>  
- **Power supply + ethernet cable** usually included in starter kits
</details>

### Step 1 – Download Umbrel
<details>
<summary>I don't know where to find Umbrel</summary>
Go to <a href="https://umbrel.com" target="_blank">umbrel.com</a> → click the big blue button "Download Umbrel OS".
</details>

### Step 2 – Flash the image with Balena Etcher
<details>
<summary>I've never flashed anything before</summary>

1. Download Balena Etcher: <a href="https://etcher.balena.io" target="_blank">etcher.balena.io</a>  
2. Start Etcher  
3. Click "Flash from file" → choose the downloaded umbrel file  
4. Click "Select target" → choose your SD card  
5. Click "Flash!" → grab a coffee (5–10 minutes)  
6. Etcher says "Flash Complete" → done!
</details>

### Step 3 – Connect everything
<details>
<summary>How do I connect the Pi?</summary>

1. Insert SD card into the Pi  
2. Connect SSD via USB (if you have one)  
3. Ethernet cable into your router  
4. Plug in power → Pi starts automatically (lights will blink)
</details>

### Step 4 – Start Umbrel
<details>
<summary>How do I reach my Umbrel?</summary>

Open your browser and type:  
http://umbrel.local  

(or find the IP address in your router app and use http://[IP-address])
</details>

### Step 5 – First setup
Choose a password → done!  
You now have at home:
- Bitcoin + Lightning node  
- Nostr relay  
- Nextcloud (your own Dropbox)  
- PhotoPrism (your own Google Photos)  
- Mastodon server (optional)  
- 40+ apps with one click

### What if it doesn't work?
<details>
<summary>I don't see umbrel.local</summary>

- Try http://[IP address of the Pi] (find in your router)  
- Or connect a screen + keyboard and log in with user "umbrel", password "moneyprintergobrrr"
</details>

Monthly cost: ≈ €3 electricity  
Security: you have the only key  
No one can ever deactivate you

---

<div style="text-align: center; margin-top: 2em; padding: 1em; background: #f0f0f0; border-radius: 8px;">
<strong>🗣️ Talk along about sovereign nodes</strong><br>
<a href="https://matrix.to/#/#openinternetmanifest:matrix.org?via=matrix.org">Open Element and join the discussion</a><br>
<small>Tip: type "Guide Raspberry Pi node" as your first message</small>
</div>

---

<div style="text-align: left; margin-top: 2em; padding: 1em; background: #f8f8f8; border-left: 4px solid #ccc; font-size: 0.9em;">

  ### Disclaimer
All guides are proposed by the community and reviewed by the OIM core team before going live.  
Nevertheless, executing technical steps remains your own responsibility.  
The Open Internet Manifest is not liable for damage, data loss, or other issues that may arise from following a guide.
</div>

---
| [← Back to thesis 7](/EN/theses/thesis-07) | [← Back to thesis 9](/EN/theses/thesis-09) | [← Back to thesis 22](/EN/theses/thesis-22) | [← Back to thesis 23](/EN/theses/thesis-23) | [← Back to thesis 25](/EN/theses/thesis-25) | [← All theses →](/EN/manifest) |
| :--- | ---: | ---: | ---: | ---: | ---: |
