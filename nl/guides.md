---
layout: default
lang: nl
title: Alle Guides
---

<div class="guides-hero">
  <h1 class="intro-title">Praktische handleidingen</h1>
  
  <h2 class="manifest-subtitle">
    Concrete stappen om te ontsnappen aan Big Tech en weer eigenaar te worden van je communicatie en data.
  </h2>
  
  <p class="intro-text">
    Van simpele account-aanmaak tot het draaien van je eigen server — begin waar je staat.
  </p>
</div>

<p>Debug: {{ guide_pages.size }} guides gevonden + 1 add = {{ guide_pages.size | plus: 1 }} items</p>

<div class="guides-grid">

<!-- + Bijdrage toevoegen als eerste card in de grid -->
<a href="#" class="guide-card contribution-card">
  <div class="guide-header">
    <span class="guide-number">+</span>
    <h3>Voeg je eigen guide toe</h3>
  </div>
  <p class="guide-teaser">
    Schrijf een nieuwe praktische handleiding – in NL, EN of andere taal.<br>
    Straks via /admin/ (dit weekend live). Nu via GitHub PR.
  </p>
  
  <div class="contribute-buttons">
    <a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/nl/guides?filename={{ 'now' | date: '%Y-%m-%d' }}-nieuwe-guide.md&value=---%0Alayout%3A%20default%0Alang%3A%20nl%0Atitle%3A%20Nieuwe%20Guide%20Titel%0Ateaser%3A%20Korte%20samenvatting...%0Adifficulty%3A%20beginner%0Aorder%3A%2099%0A---%0A%0A## Inleiding%0A%0ASchrijf%20hier..." class="btn-contribute nl">
      Start nieuwe Guide (NL)
    </a>
    
    <a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/en/guides?filename={{ 'now' | date: '%Y-%m-%d' }}-new-guide.md&value=---%0Alayout%3A%20default%0Alang%3A%20en%0Atitle%3A%20New%20Guide%0Ateaser%3A%20Short%20summary...%0Adifficulty%3A%20beginner%0Aorder%3A%2099%0A---%0A%0A## Intro..." class="btn-contribute en">
      New Guide (EN)
    </a>
  </div>
  
  <span class="read-more">Maak PR →</span>
</a>

  <!-- Bestaande guides loop -->
{% assign all_guide_pages = site.pages | where_exp: "p", "p.path contains '/nl/guides/'" %}
{% assign guide_pages = all_guide_pages | where_exp: "item", "item.title != nil and item.title != '' and item.url != page.url" | sort: "order" %}

<p>Debug: totaal pages met '/nl/guides/' in path = {{ all_guide_pages.size }}</p>
<p>Debug: na filter title + niet self = {{ guide_pages.size }} → totaal items (incl add-card) = {{ guide_pages.size | plus: 1 }}</p>
  {% for guide in guide_pages %}
    {% if guide.url != page.url and guide.title and guide.title != "" %}
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
    {% endif %}
  {% endfor %}

  {% if guide_pages.size == 0 or guide_pages.size == 1 %}
    <p style="color: #f66; text-align:center;">(debug) Geen guides gevonden of alleen deze overzichtspagina zelf.</p>
  {% endif %}

</div>