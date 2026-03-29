---
layout: default
lang: en
title: Reality vs Narrative - Social Posts
---

<div class="overview-hero">
  <h1 class="intro-title">Reality vs Narrative</h1>
  
  <h2 class="manifest-subtitle">
    Daily confrontation between what we're told and what actually happens.
  </h2>
  
  <p class="intro-text">
    Every day a teaser (in the evening) and a full RVN analysis (in the morning) — follow day by day or dive into a specific moment.
  </p>
</div>

<div class="social-grid">

  <!-- Unified add-card -->
  {% assign now_date = 'now' | date: '%Y-%m-%d' %}

  {% assign rvn_template_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/en?filename=" | append: now_date | append: "-rvn-day.md&value=---%0Alang%3A%20en%0Aday%3A%20%22Enter%20day%20number%22%0Arvn_title%3A%20Reality%20vs%20Narrative%0Arvn_teaser%3A%20Short%20content%20for%20the%20RVN...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Or%20Monero%2FBTC%20address%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Support%20the%20author%20of%20this%20RVN%22%20%23%20Optional%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Reality%0A%0A...%0A%0A## Narrative%0A%0A...%0A%0A## Analysis%0A%0A..." %}

  {% assign teaser_template_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/en?filename=" | append: now_date | append: "-teaser-day.md&value=---%0Alang%3A%20en%0Aday%3A%20%22Enter%20day%20number%22%0Ateaser_title%3A%20Evening%20Teaser%20–%20Day%20%0Ateaser_text%3A%20Highlights%20for%20the%20evening...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Or%20Monero%2FBTC%20address%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Support%20the%20author%20of%20this%20teaser%22%20%23%20Optional%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Evening%20Teaser%0A%0AHighlights%20for%20the%20evening..." %}

  {% capture add_extra_content %}
    <div class="rvn-title">Write a new RVN-day in EN, NL or other language. Soon via /admin/, now via GitHub PR.</div>
    
    <div class="contribute-buttons">
      <a href="{{ rvn_template_url }}" class="btn-contribute" target="_blank" rel="noopener">Add RVN</a>
    </div>
    
    <div class="divider"></div>
    
    <div class="teaser-title">Evening Teaser - Day</div>
    
    <div class="contribute-buttons">
      <a href="{{ teaser_template_url }}" class="btn-contribute" target="_blank" rel="noopener">Add Teaser</a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution" 
    url="#" 
    title="Add new RVN / Teaser day" 
    number="+" 
    extra_class="contribution-card social-card" 
    extra_content=add_extra_content 
  %}

  <!-- Social posts loop -->
  {% assign all_social_pages = site.pages | where: "lang", "en" | where_exp: "item", "item.path contains 'social-posts/'" %}
  {% assign rvn_only = all_social_pages | where_exp: "item", "item.path contains '-rvn'" %}
  {% assign teaser_only = all_social_pages | where_exp: "item", "item.path contains '-teaser'" %}

  {% assign social_posts = rvn_only | concat: teaser_only | uniq %}

  {% assign unique_days = social_posts | map: "day" | uniq | sort_natural %}

  {% for this_day in unique_days %}
    {% if this_day == "" or this_day == nil %}{% continue %}{% endif %}

    {% assign day_rvn = nil %}
    {% assign day_teaser = nil %}

    {% for post in social_posts %}
      {% if post.day == this_day %}
        {% if post.path contains "-rvn" %}
          {% assign day_rvn = post %}
        {% elsif post.path contains "-teaser" %}
          {% assign day_teaser = post %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% assign card_title = "Day " | append: this_day %}

    {% if day_rvn %}
      {% assign card_title = day_rvn.rvn_title | default: day_rvn.title | default: card_title %}
      {% assign card_url = day_rvn.url | relative_url %}
      {% assign rvn_teaser = day_rvn.rvn_teaser | default: "No RVN content yet for day " | append: this_day | strip_html | truncatewords: 45 %}
    {% else %}
      {% assign rvn_teaser = "No RVN yet for day " | append: this_day %}
      {% assign card_url = "#" %}
    {% endif %}

    {% if day_teaser %}
      {% assign teaser_part = day_teaser.teaser_title | default: "Evening Teaser – Day " | append: this_day %}
      {% assign teaser_preview = day_teaser.teaser_text | default: day_teaser.teaser | default: "No teaser yet" | strip_html | truncatewords: 28 %}
    {% else %}
      {% assign teaser_part = "Evening Teaser – Day " | append: this_day %}
      {% assign teaser_preview = "No teaser yet" %}
    {% endif %}

    {% capture extra_content %}
      <p class="rvn-teaser">{{ rvn_teaser }}</p>
      <div class="divider"></div>
      <div class="teaser-title">
        {% if day_teaser %}
          <a href="{{ day_teaser.url | relative_url }}">{{ teaser_part }}</a>
        {% else %}
          {{ teaser_part }}
        {% endif %}
      </div>
      <p class="teaser-preview">{{ teaser_preview }}</p>
    {% endcapture %}

  

    {% include card.html 
      type="social" 
      url=card_url 
      title=card_title 
      number=this_day 
      extra_class="social-card" 
      extra_content=extra_content 
    %}
  {% endfor %}

</div>