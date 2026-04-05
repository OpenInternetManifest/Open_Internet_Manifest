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

  <!-- Add Guide contribution card - Updated -->
  {% capture add_extra_content_guides %}
    <div class="rvn-title">Schrijf een nieuwe praktische gids – in EN, NL of een andere taal.</div>
    
    <div class="contribute-buttons">
      <a href="/nl/contribute/" class="btn-contribute" target="_blank" rel="noopener">Gids toevoegen</a>
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