---
layout: default
lang: en
title: All Guides
---

<div class="overview-hero">
  <h1 class="intro-title">Practical Guides</h1>
  
  <h2 class="manifest-subtitle">
    Concrete steps to escape Big Tech and take back ownership of your communication and data.
  </h2>
  
  <p class="intro-text">
    From simple account creation to running your own server — start wherever you are.
  </p>
</div>

{% assign guide_pages = site.guides | where: "lang", "en" | sort: "order" %}<div class="guides-grid">

  <!-- Add Guide contribution card - Updated to new contribute page -->
  {% capture add_extra_content_guides %}
    <div class="rvn-title">Write a new practical guide – in EN, NL or another language.</div>
    
    <div class="contribute-buttons">
      <a href="/en/contribute/" class="btn-contribute" target="_blank" rel="noopener">Add Guide</a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution-guide" 
    title="Add your own guide" 
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
  {% endfor %}</div>

