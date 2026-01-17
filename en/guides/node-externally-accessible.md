---
layout: default
lang: en
title: Make Your Node Externally Accessible
permalink: /en/guides/make-node-accessible/
---

# Make Your Node Externally Accessible – Choose the Method That Suits You

Your Umbrel node is now running locally (http://umbrel.local), but how do you access it securely from your phone or laptop when you're away from home? There are several ways, from super simple to advanced. We recommend starting with the easiest one.

### Which Method Should You Choose?

| Method                           | Difficulty | Speed   | Privacy/Security | When to Choose?                              | Setup Time     | Platform Notes                        |
|----------------------------------|------------|---------|------------------|----------------------------------------------|----------------|---------------------------------------|
| **Tor Onion** (recommended start) | ★☆☆☆☆     | Slow    | Maximum          | Maximum privacy, no extra account            | 2 minutes      | Android good, iPhone slow (Orbot)    |
| **Tailscale HTTP**               | ★★☆☆☆     | Fast    | High (WireGuard) | Daily use, file sync from phone              | 5-10 minutes   | Works on all devices                  |
| **Tailscale HTTPS**              | ★★★★☆     | Fast    | Very high        | Green padlock, apps requiring HTTPS          | 15-30 minutes  | Requires terminal (see advanced)      |
| Other (Zerotier, Headscale, etc.)| ★★★★★     | Variable| High             | No Tailscale account                         | 30+ minutes    | For hardcore decentralists            |

**Why start with Tor?** No hassle with accounts or opening ports.  
**Why upgrade to Tailscale?** Much faster for Nextcloud sync, photo uploads, etc.

### Option 1: Tor Onion – The Easiest & Most Private Way

**Why choose this?**  
No extra installations, no account, no ports open → maximum privacy. Works everywhere (behind CG-NAT, carrier NAT).

**Drawbacks:** Slow for large files (photos, videos).

**Steps (2 minutes):**

1. Open Umbrel dashboard (http://umbrel.local).
2. Go to **Settings** → **Advanced Settings** → **Remote Access**.
3. Enable **Via Tor**.
4. Umbrel generates an .onion link (e.g., http://long-string.onion).
5. Copy the link and store it securely.

**Access from your device:**

- **Android:** Install Tor Browser (Play Store) → paste .onion link → dashboard opens.
- **iPhone:** Install Onion Browser or Orbot (App Store). **Note:** Orbot often loads slowly or is unstable on iOS. Try Onion Browser as alternative.
- **Laptop/PC:** Download Tor Browser (torproject.org) → paste link.

For Nextcloud: http://[your-onion]/nextcloud (use Tor Browser).  
For mobile Nextcloud app: Tor not directly supported → use web version in Tor Browser.

**Screenshot:** [Insert screenshot here of Umbrel: Remote Access → Tor toggle + .onion link]

**Tip:** Bookmark the .onion link in Tor Browser. Test on laptop first if it feels slow on phone.

### Option 2: Tailscale HTTP – Faster for Daily Use (No Terminal Required)

**Why?**  
Fast (WireGuard), nice link (umbrel.your-tailnet.ts.net), secure end-to-end encrypted. No ports open.

**Steps:**

1. Umbrel App Store → search “Tailscale” → Install.
2. Open Tailscale app → Authenticate → log in with Google/Apple/GitHub (free account).
3. Toggle VPN on.
4. On phone/laptop: login.tailscale.com → log in with same account → see your “umbrel” node.
5. Click the node → copy **Magic DNS name** (e.g., umbrel.tail63975b.ts.net).
6. Open browser → **http://umbrel.tail63975b.ts.net** (without https!).
7. Dashboard loads → Nextcloud at http://.../nextcloud.

**Mobile:**
- Install Tailscale app (iOS/Android) → login → auto-connect.
- Nextcloud app: server = http://umbrel.tail63975b.ts.net/nextcloud.

**Screenshot:** [Insert screenshot here of Tailscale admin → Magic DNS name]

**Warning:** Some apps require HTTPS → choose Option 3 or stick with Tor.

### Option 3: Tailscale HTTPS – Advanced (Green Padlock)

**Warning:** This requires terminal commands. Not for beginners. HTTP is often sufficient (secure via Tailscale).

**Steps:**

1. Umbrel App Store → install & authenticate Tailscale (as in Option 2).
2. Settings → Advanced → Terminal → select App: Tailscale.
3. Run: `tailscale serve 8080` (or 8081 if Umbrel uses 8081 – check with netstat in main terminal).
4. Check: `tailscale serve status` → see proxy to 127.0.0.1:8080.
5. Test: https://umbrel.tail63975b.ts.net (should now load with green padlock).

**Make persistent (optional):** Run in screen or create startup script via Portainer.

**Common Mistakes & Fixes:**
- Permission denied on docker? Use sudo: `sudo docker ps | grep nextcloud` → container name is often nextcloud_web_1.
- “Access through untrusted domain”? Fix trusted_domains: