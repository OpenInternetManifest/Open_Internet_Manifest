---
layout: default
lang: nl
title: De 100 Theses
---

<div class="overview-hero">
  <h1 class="intro-title">De 100 Theses</h1>
  
  <h2 class="manifest-subtitle">
    Kernprincipes voor een vrij, open en gedecentraliseerd internet.
  </h2>
  
  <p class="intro-text">
    Fundamentele uitspraken over technologie, macht, privacy en menselijke vrijheid.
  </p>
</div>

{% assign thesis_pages = site.theses | where: "lang", "nl" | sort: "nummer" %}

<div class="theses-grid">

  <!-- Add Thesis contribution card -->
  {% assign now_date = 'now' | date: '%Y-%m-%d' %}
  {% assign contrib_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_theses/nl?filename=" | append: now_date | append: "-nieuwe-thesis.md&value=---%0Alayout%3A%20default%0Alang%3A%20nl%0Atitle%3A%20Nieuwe%20Thesis%20Titel%0Ateaser%3A%20Korte%20samenvatting...%0Anummer%3A%2099%0Aslug%3A%20nieuwe-thesis-slug%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Steun%20de%20auteur%20van%20deze%20thesis%22%20%23%20Optioneel%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A##%20Thesis%0A%0ASchrijf%20hier%20je%20thesis..." %}

  {% capture add_extra_content_theses %}
    <div class="rvn-title">Draag bij met een nieuwe thesis aan het manifest – in EN, NL of een andere taal. Binnenkort via /admin/, nu via GitHub PR.</div>
    
    <div class="contribute-buttons">
      <a href="{{ contrib_url }}" class="btn-contribute" target="_blank" rel="noopener">Thesis toevoegen</a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution-thesis" 
    title="Schrijf je eigen thesis" 
    extra_class="contribution-card" 
    extra_content=add_extra_content_theses 
  %}

  {% for thesis in thesis_pages %}
    {% include card.html 
      type="thesis" 
      item=thesis 
      number=thesis.nummer 
      title=thesis.title 
      teaser=thesis.teaser 
    %}
  {% endfor %}

</div>