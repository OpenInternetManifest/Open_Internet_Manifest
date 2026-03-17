---
layout: default
lang: en
title: All Theses
---

<div class="overview-hero">
  <h1 class="intro-title">The first 30 theses are ready</h1>
  
  <h2 class="manifest-subtitle">
    This manifesto is alive — it grows through contributions from people like you.
  </h2>
  
  <p class="intro-text">
    100 theses for a free, open and unalienable internet. Start wherever you want — or read from the beginning.
  </p>
</div>

<!-- Debug first -->
<p style="color: lime; text-align: center; font-weight: bold; margin: 2rem 0;">
  Debug: total pages with '/en/theses/' in path = {{ site.pages | where_exp: "p", "p.path contains '/en/theses/'" | size }}
</p>

{% assign thesis_pages = site.theses | where: "lang", "en" | sort: "order" %}

<p style="color: lime; text-align: center;">
  Debug: theses (EN) loaded = {{ thesis_pages.size }} items
</p>

<div class="theses-grid">

<!-- + Add contribution as first card in the grid – entire card clickable -->
<a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_theses/en?filename={{ 'now' | date: '%Y-%m-%d' }}-new-thesis.md&value=---%0Alayout%3A%20default%0Alang%3A%20en%0Atitle%3A%20New%20Thesis%20Title%0Ateaser%3A%20Short%20summary...%0Aprogress%3A%200%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Or%20Monero%2FBTC%20address%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Support%20the%20author%20of%20this%20thesis%22%20%23%20Optional%2C%20otherwise%20default%20text%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Thesis%0A%0AWrite%20your%20thesis%20here..." 
   class="thesis-card contribution-card">
  <div class="thesis-header">
    <span class="thesis-number">+</span>
    <h3>Add your own thesis</h3>
  </div>
  <p class="thesis-teaser">
    Write a new thesis for the manifesto – in EN, NL or other language.<br>
    Soon via /admin/, now via GitHub PR.
  </p>
  
  <span class="read-more">Add contribution →</span>
</a>

  {% for thesis in thesis_pages %}
    {% if thesis.url != page.url %}
      <a href="{{ thesis.url | relative_url }}" class="thesis-card">
        <div class="thesis-header">
          <span class="thesis-number">{{ forloop.index }}</span>
          <h3>{{ thesis.title }}</h3>
        </div>
        <p class="thesis-teaser">{{ thesis.teaser | default: "Read the full thesis." }}</p>
        
        <!-- Progress label top right -->
        <span class="thesis-progress">Thesis {{ forloop.index }}/100</span>
        
        <span class="read-more">Read full →</span>
      </a>
    {% endif %}
  {% endfor %}

  {% if thesis_pages.size == 0 %}
    <p style="color: #f66; text-align:center; padding: 2rem;">
      (debug) No theses found in collection.<br>
      Check: do the files exist in _theses/en/? Do they have frontmatter with lang: en and order:?
    </p>
  {% endif %}

</div>