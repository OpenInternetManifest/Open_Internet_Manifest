---
layout: default
lang: nl
title: Alle Guides
---
<ul>
{% for p in site.pages %}
  {% if p.path contains '/nl/guides/' %}
    <li>{{ p.path }} – title: {{ p.title | default: 'geen' }} – order: {{ p.order | default: 'geen' }}</li>
  {% endif %}
{% endfor %}
</ul>

<div class="guides-hero">
  <h1 class="intro-title">Praktische handleidingen</h1>
  
  <h2 class="manifest-subtitle">
    Concrete stappen om te ontsnappen aan Big Tech en weer eigenaar te worden van je communicatie en data.
  </h2>
  
  <p class="intro-text">
    Van simpele account-aanmaak tot het draaien van je eigen server — begin waar je staat.
  </p>
</div>

{% assign guide_pages = site.guides | where: "lang", "nl" | sort: "order" %}

<div class="guides-grid">
<!-- + Bijdrage toevoegen als eerste card in de grid – volledige card clickable -->
<a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_guides/nl?filename={{ 'now' | date: '%Y-%m-%d' }}-nieuwe-guide.md&value=---%0Alayout%3A%20default%0Alang%3A%20nl%0Atitle%3A%20Nieuwe%20Guide%20Titel%0Ateaser%3A%20Korte%20samenvatting...%0Adifficulty%3A%20beginner%0Aorder%3A%2099%0Aslug%3A%20nieuwe-guide-slug%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fvoorbeeldlink%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Ondersteun%20de%20auteur%20van%20deze%20thesis%22%20%23%20Optioneel%2C%20anders%20default%20tekst%0A%23%20Integriteit%20hashes%20(automatisch%20toegevoegd%20na%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatisch%20toegevoegd%20na%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Inleiding%0A%0ASchrijf%20hier..." 
   class="guide-card contribution-card">
  <div class="guide-header">
    <span class="guide-number">+</span>
    <h3>Voeg je eigen guide toe</h3>
  </div>
  <p class="guide-teaser">
    Schrijf een nieuwe praktische handleiding – in NL, EN of andere taal.<br>
    Straks via /admin/, nu via GitHub PR.
  </p>
  
  <span class="read-more">Bijdrage toevoegen →</span>
</a>
  

  {% for guide in guide_pages %}
    <a href="{{ guide.url | relative_url }}" class="guide-card" data-difficulty="{{ guide.difficulty | default: 'beginner' }}">
      <div class="guide-header">
        <span class="guide-number">{{ forloop.index }}</span>
        <h3>{{ guide.title }}</h3>
      </div>
      <p class="guide-teaser">{{ guide.teaser | default: "Praktische stap-voor-stap handleiding." }}</p>
      
      <span class="difficulty-banner {{ guide.difficulty | default: 'beginner' }}">
        {% case guide.difficulty %}
          {% when 'beginner' %}Beginner
          {% when 'gemiddeld' %}Gemiddeld
          {% when 'gevorderd' %}Gevorderd
          {% else %}Beginner
        {% endcase %}
      </span>
      
      <span class="read-more">Lees de guide →</span>
    </a>
  {% endfor %}

  {% if guide_pages.size == 0 %}
    <p style="color: #f66; text-align:center;">(debug) Geen guides in collection – check _config.yml en frontmatter</p>
  {% endif %}

</div>