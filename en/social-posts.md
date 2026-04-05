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

  <!-- Add RVN/Teaser contribution card - Clean version -->
  {% capture add_extra_content %}
    <div class="add-description">
      Write a new RVN or Evening Teaser in EN, NL or another language.
    </div>
    
    <div class="contribute-buttons">
      <a href="/en/contribute/" class="btn-contribute" target="_blank" rel="noopener">
        Add RVN / Teaser
      </a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution" 
    title="Add new RVN / Teaser day" 
    number="+" 
    extra_class="contribution-card social-card" 
    extra_content=add_extra_content 
  %}

    <!-- SOCIAL POSTS LOOP - Nieuwste eerst, sortering op bestandsnaam (simpel & robuust) -->
  {% assign social_posts = site.social-posts | where: "lang", "en" %}

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

    {% assign card_title = "Day " | append: this_day %}

    {% if day_rvn %}
      {% assign card_title = day_rvn.rvn_title | default: day_rvn.title | default: card_title %}
      {% assign card_url = day_rvn.url | relative_url %}
      {% assign rvn_teaser = day_rvn.rvn_teaser | default: day_rvn.teaser | default: "No RVN content yet for day "  | strip_html | truncatewords: 45 %}
    {% else %}
      {% assign rvn_teaser = "No RVN yet for day " | append: this_day %}
      {% assign card_url = "#" %}
    {% endif %}

    {% if day_teaser %}
      {% assign teaser_part = day_teaser.teaser_title | default: "Evening Teaser – Day "  %}
      {% assign teaser_preview = day_teaser.teaser_text | default: day_teaser.teaser | default: "No teaser yet" | strip_html | truncatewords: 28 %}
    {% else %}
      {% assign teaser_part = "Evening Teaser – Day " | append: this_day %}
      {% assign teaser_preview = "No teaser yet" %}
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