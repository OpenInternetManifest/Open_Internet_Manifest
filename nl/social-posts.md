---
layout: default
lang: nl
title: Realiteit vs Narratief - Social Posts
---

<div class="overview-hero">
  <h1 class="intro-title">Realiteit vs Narratief</h1>
  
  <h2 class="manifest-subtitle">
    Dagelijkse confrontatie tussen wat ons verteld wordt en wat er werkelijk gebeurt.
  </h2>
  
  <p class="intro-text">
    Elke dag een teaser ('s avonds) en een volledige RVN-analyse ('s ochtends) — volg dag voor dag of duik in een specifiek moment.
  </p>
</div>

<div class="social-grid">

  <!-- Unified add-card -->
  {% assign now_date = 'now' | date: '%Y-%m-%d' %}

  {% assign rvn_template_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/nl?filename=" | append: now_date | append: "-rvn-dag.md&value=---%0Alang%3A%20nl%0Aday%3A%20%22Vul%20dagnummer%20in%22%0Arvn_title%3A%20Realiteit%20vs%20Narratief%0Arvn_teaser%3A%20Korte%20inhoud%20voor%20de%20RVN...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Steun%20de%20auteur%20van%20deze%20RVN%22%20%23%20Optioneel%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A##%20Realiteit%0A%0A...%0A%0A##%20Narratief%0A%0A...%0A%0A##%20Analyse%0A%0A..." %}

  {% assign teaser_template_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/nl?filename=" | append: now_date | append: "-teaser-dag.md&value=---%0Alang%3A%20nl%0Aday%3A%20%22Vul%20dagnummer%20in%22%0Ateaser_title%3A%20Avond%20Teaser%20–%20Dag%20%0Ateaser_text%3A%20Highlights%20voor%20de%20avond...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Steun%20de%20auteur%20van%20deze%20teaser%22%20%23%20Optioneel%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A##%20Avond%20Teaser%0A%0AHighlights%20voor%20de%20avond..." %}

  {% capture add_extra_content %}
    <div class="rvn-title">Schrijf een nieuwe RVN-dag in EN, NL of een andere taal. Binnenkort via /admin/, nu via GitHub PR.</div>
    
    <div class="contribute-buttons">
      <a href="{{ rvn_template_url }}" class="btn-contribute" target="_blank" rel="noopener">RVN toevoegen</a>
    </div>
    
    <div class="divider"></div>
    
    <div class="teaser-title">Avond Teaser - Dag</div>
    
    <div class="contribute-buttons">
      <a href="{{ teaser_template_url }}" class="btn-contribute" target="_blank" rel="noopener">Teaser toevoegen</a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution" 
    url="#" 
    title="Nieuwe RVN / Teaser dag toevoegen" 
    number="+" 
    extra_class="contribution-card social-card" 
    extra_content=add_extra_content 
  %}

  <!-- SOCIAL POSTS LOOP - Nieuwste eerst, sortering op bestandsnaam -->
  {% assign social_posts = site.social-posts | where: "lang", "nl" %}

  <!-- Verzamel dagen uit bestandsnaam -->
  {% assign day_list = "" | split: "" %}
  {% for post in social_posts %}
    {% if post.path contains "day-" %}
      {% assign filename = post.path | split: "/" | last | split: "." | first %}
      {% assign day_num = filename | remove: "day-" | remove: "-rvn" | remove: "-teaser" | strip %}
      {% if day_num and day_num != "" %}
        {% assign day_list = day_list | push: day_num %}
      {% endif %}
    {% endif %}
  {% endfor %}

  {% assign unique_days = day_list | uniq | sort_natural | reverse %}

  {% for this_day in unique_days %}
    {% if this_day == "" or this_day == nil %}{% continue %}{% endif %}

    {% assign day_rvn = nil %}
    {% assign day_teaser = nil %}

    {% for post in social_posts %}
      {% assign filename = post.path | split: "/" | last %}
      {% if filename contains this_day %}
        {% if filename contains "-rvn" %}
          {% assign day_rvn = post %}
        {% elsif filename contains "-teaser" %}
          {% assign day_teaser = post %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% assign card_title = "Dag " | append: this_day %}

    {% if day_rvn %}
      {% assign card_title = day_rvn.rvn_title | default: day_rvn.title | default: card_title %}
      {% assign card_url = day_rvn.url | relative_url %}
      {% assign rvn_teaser = day_rvn.rvn_teaser | default: day_rvn.teaser | default: "Nog geen RVN voor dag "  | strip_html | truncatewords: 45 %}
    {% else %}
      {% assign rvn_teaser = "Nog geen RVN voor dag "  %}
      {% assign card_url = "#" %}
    {% endif %}

    {% if day_teaser %}
      {% assign teaser_part = day_teaser.teaser_title | default: "Avond Teaser – Dag " %}
      {% assign teaser_preview = day_teaser.teaser_text | default: day_teaser.teaser | default: "Nog geen teaser" | strip_html | truncatewords: 28 %}
    {% else %}
      {% assign teaser_part = "Avond Teaser – Dag " | append: this_day %}
      {% assign teaser_preview = "Nog geen teaser" %}
    {% endif %}

    {% capture extra_content %}
      <div class="rvn-title">
        {% if day_rvn %}
          <a href="{{ day_rvn.url | relative_url }}">{{ card_title }}</a>
        {% else %}
          {{ card_title }}
        {% endif %}
      </div>

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