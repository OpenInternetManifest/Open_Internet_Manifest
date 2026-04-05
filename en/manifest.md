---
layout: default
lang: en
title: The 100 Theses
---

<div class="overview-hero">
  <h1 class="intro-title">The 100 Theses</h1>
  
  <h2 class="manifest-subtitle">
    Core principles for a free, open and decentralized internet.
  </h2>
  
  <p class="intro-text">
    Fundamental statements about technology, power, privacy and human freedom.
  </p>
</div>

{% assign thesis_pages = site.theses | where: "lang", "en" | sort: "nummer" %}

<div class="theses-grid">

  <!-- Add Thesis contribution card - Updated to new contribute page -->
  {% capture add_extra_content_theses %}
    <div class="rvn-title">Contribute a new thesis to the manifesto – in EN, NL or another language.</div>
    
    <div class="contribute-buttons">
      <a href="/en/contribute/" class="btn-contribute" target="_blank" rel="noopener">Add Thesis</a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution-thesis" 
    title="Add your own thesis" 
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