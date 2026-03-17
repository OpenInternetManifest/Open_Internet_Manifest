---
layout: default
lang: nl
title: Alle Theses
---

<div class="overview-hero">
  <h1 class="intro-title">De eerste 30 theses zijn klaar</h1>
  
  <h2 class="manifest-subtitle">
    Dit manifest leeft — het groeit door bijdragen van mensen zoals jij.
  </h2>
  
  <p class="intro-text">
    100 theses voor een vrij, open en onvervreemdbaar internet. Begin waar je wilt — of lees vanaf het begin.
  </p>
</div>

<!-- Debug eerst -->
<p style="color: lime; text-align: center; font-weight: bold; margin: 2rem 0;">
  Debug: totaal pages met '/nl/theses/' in path = {{ site.pages | where_exp: "p", "p.path contains '/nl/theses/'" | size }}
</p>

{% assign thesis_pages = site.theses | where: "lang", "nl" | sort: "order" %}

<p style="color: lime; text-align: center;">
  Debug: theses (NL) geladen = {{ thesis_pages.size }} items
</p>

<div class="theses-grid">

<!-- + Bijdrage toevoegen als eerste card in de grid – volledige card clickable -->
<a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_theses/nl?filename={{ 'now' | date: '%Y-%m-%d' }}-nieuwe-these.md&value=---%0Alayout%3A%20default%0Alang%3A%20nl%0Atitle%3A%20Nieuwe%20These%20Titel%0Ateaser%3A%20Korte%20samenvatting...%0Aprogress%3A%200%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fvoorbeeldlink%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Ondersteun%20de%20auteur%20van%20deze%20these%22%20%23%20Optioneel%2C%20anders%20default%20tekst%0A%23%20Integriteit%20hashes%20(automatisch%20toegevoegd%20na%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatisch%20toegevoegd%20na%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## These%0A%0ASchrijf%20je%20these%20hier..." 
   class="thesis-card contribution-card">
  <div class="thesis-header">
    <span class="thesis-number">+</span>
    <h3>Voeg je eigen thesis toe</h3>
  </div>
  <p class="thesis-teaser">
    Schrijf een nieuwe thesis voor het manifest – in NL, EN of andere taal.<br>
    Straks via /admin/, nu via GitHub PR.
  </p>
  
  <span class="read-more">Bijdrage toevoegen →</span>
</a>

  {% for thesis in thesis_pages %}
    {% if thesis.url != page.url %}
      <a href="{{ thesis.url | relative_url }}" class="thesis-card">
        <div class="thesis-header">
          <span class="thesis-number">{{ forloop.index }}</span>
          <h3>{{ thesis.title }}</h3>
        </div>
        <p class="thesis-teaser">{{ thesis.teaser | default: "Lees de volledige these." }}</p>
        
        <!-- Progress label rechtsboven -->
        <span class="thesis-progress">Thesis {{ forloop.index }}/100</span>
        
        <span class="read-more">Lees volledig →</span>
      </a>
    {% endif %}
  {% endfor %}

  {% if thesis_pages.size == 0 %}
    <p style="color: #f66; text-align:center; padding: 2rem;">
      (debug) Geen theses gevonden in collection.<br>
      Controleer: bestaan de bestanden in _theses/nl/? Hebben ze frontmatter met lang: nl en order:?
    </p>
  {% endif %}

</div>