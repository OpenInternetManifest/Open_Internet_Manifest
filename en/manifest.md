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

  <!-- Add Thesis contribution card -->
  {% assign now_date = 'now' | date: '%Y-%m-%d' %}
  {% assign contrib_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_theses/en?filename=" | append: now_date | append: "-new-thesis.md&value=---%0Alayout%3A%20default%0Alang%3A%20en%0Atitle%3A%20New%20Thesis%20Title%0Ateaser%3A%20Short%20summary...%0Anummer%3A%2099%0Aslug%3A%20new-thesis-slug%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Or%20Monero%2FBTC%20address%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Support%20the%20author%20of%20this%20thesis%22%20%23%20Optional%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A##%20Thesis%0A%0AWrite%20your%20thesis%20here..." %}

  {% capture add_extra_content_theses %}
    <div class="rvn-title">Contribute a new thesis to the manifesto – in EN, NL or other language. Soon via /admin/, now via GitHub PR.</div>
    
    <div class="contribute-buttons">
      <a href="{{ contrib_url }}" class="btn-contribute" target="_blank" rel="noopener">Add Thesis</a>
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