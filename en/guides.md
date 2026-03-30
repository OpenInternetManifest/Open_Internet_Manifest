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

  <!-- Add Guide contribution card -->
  {% assign now_date = 'now' | date: '%Y-%m-%d' %}
  {% assign contrib_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_guides/en?filename=" | append: now_date | append: "-new-guide.md&value=---%0Alayout%3A%20default%0Alang%3A%20en%0Atitle%3A%20New%20Guide%20Title%0Ateaser%3A%20Short%20summary...%0Adifficulty%3A%20beginner%0Aorder%3A%2099%0Aslug%3A%20new-guide-slug%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Or%20Monero%2FBTC%20address%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Support%20the%20author%20of%20this%20guide%22%20%23%20Optional%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A##%20Introduction%0A%0AWrite%20your%20content%20here..." %}  {% capture add_extra_content_guides %}
    <div class="rvn-title">Write a new practical guide – in EN, NL or other language. Soon via /admin/, now via GitHub PR.</div><div class="contribute-buttons">
  <a href="{{ contrib_url }}" class="btn-contribute" target="_blank" rel="noopener">Add Guide</a>
</div>  {% endcapture %}  {% include card.html 
    type="contribution-guide" 
    title="Add your own guide" 
    extra_class="contribution-card" 
    extra_content=add_extra_content_guides 
  %}  {% for guide in guide_pages %}
    {% include card.html 
      type="guide" 
      item=guide 
      number=forloop.index 
      title=guide.title 
      teaser=guide.teaser 
      difficulty=guide.difficulty 
    %}
  {% endfor %}</div>

