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

    <!-- Add Thesis contribution card - Updated to new contribute page -->
  {% capture add_extra_content_theses %}
    <div class="rvn-title">Draag bij met een nieuwe thesis aan het manifest – in EN, NL of een andere taal.</div>
    
    <div class="contribute-buttons">
      <a href="/nl/contribute/" class="btn-contribute" target="_blank" rel="noopener">Thesis toevoegen</a>
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