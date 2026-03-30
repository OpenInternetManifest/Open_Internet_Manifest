---
layout: default
lang: nl
title: Alle Gidsen
---

<div class="overview-hero">
  <h1 class="intro-title">Praktische Gidsen</h1>
  
  <h2 class="manifest-subtitle">
    Concrete stappen om los te komen van Big Tech en weer eigenaar te worden van je communicatie en data.
  </h2>
  
  <p class="intro-text">
    Van een simpel account aanmaken tot het draaien van je eigen server — begin waar je nu bent.
  </p>
</div>

{% assign guide_pages = site.guides | where: "lang", "nl" | sort: "order" %}

<div class="guides-grid">

  <!-- Add Guide contribution card -->
  {% assign now_date = 'now' | date: '%Y-%m-%d' %}
  {% assign contrib_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_guides/nl?filename=" | append: now_date | append: "-nieuwe-gids.md&value=---%0Alayout%3A%20default%0Alang%3A%20nl%0Atitle%3A%20Nieuwe%20Gids%20Titel%0Ateaser%3A%20Korte%20samenvatting...%0Adifficulty%3A%20beginner%0Aorder%3A%2099%0Aslug%3A%20nieuwe-gids-slug%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Steun%20de%20auteur%20van%20deze%20gids%22%20%23%20Optioneel%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A##%20Inleiding%0A%0ASchrijf%20hier%20je%20inhoud..." %}

  {% capture add_extra_content_guides %}
    <div class="rvn-title">Schrijf een nieuwe praktische gids – in EN, NL of een andere taal. Binnenkort via /admin/, nu via GitHub PR.</div>
    
    <div class="contribute-buttons">
      <a href="{{ contrib_url }}" class="btn-contribute" target="_blank" rel="noopener">Gids toevoegen</a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution-guide" 
    title="Schrijf je eigen gids" 
    extra_class="contribution-card" 
    extra_content=add_extra_content_guides 
  %}

  {% for guide in guide_pages %}
    {% include card.html 
      type="guide" 
      item=guide 
      number=forloop.index 
      title=guide.title 
      teaser=guide.teaser 
      difficulty=guide.difficulty 
    %}
  {% endfor %}

</div>