---
layout: default
lang: en
title: Reality vs Narrative – Social Posts
---

<div class="social-posts-hero">
  <h1 class="intro-title">Reality vs Narrative</h1>
  
  <h2 class="manifest-subtitle">
    Daily confrontation between what we're told and what actually happens.
  </h2>
  
  <p class="intro-text">
    Every day a teaser (in the evening) and a full RVN analysis (in the morning) — follow day by day or dive into a specific moment.
  </p>
</div>

<div class="social-grid">

  <!-- + Add contribution as first card – exact grid-match with normal cards -->
  <div class="social-card contribution-card">
    <div class="social-header">
      <span class="social-number">+</span>
    </div>
  <!-- RVN title placeholder -->
    <div class="rvn-title">
      Write a new RVN-day in EN, NL or other language. Soon via /admin/, now via GitHub PR.
    </div>
  <!-- Button RVN – above divider -->
    <div class="contribute-buttons rvn">
      <a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/en?filename={{ 'now' | date: '%Y-%m-%d' }}-rvn-day.md&value=---%0Alang%3A%20en%0Aday%3A%20%22Enter%20day%20number%22%0Arvn_title%3A%20Reality%20vs%20Narrative%0Arvn_teaser%3A%20Short%20content%20for%20the%20RVN...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Or%20Monero%2FBTC%20address%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Support%20the%20author%20of%20this%20RVN%22%20%23%20Optional%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Reality%0A%0A...%0A%0A## Narrative%0A%0A...%0A%0A## Analysis%0A%0A..." 
         class="btn-contribute rvn">
        Add RVN
      </a>
    </div>
    <!-- Divider -->
    <div class="divider"></div>
    <!-- Teaser title placeholder -->
    <div class="teaser-title">
      Evening Teaser – Day
    </div>
    <!-- Button teaser – below divider -->
    <div class="contribute-buttons teaser">
      <a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/en?filename={{ 'now' | date: '%Y-%m-%d' }}-teaser-day.md&value=---%0Alang%3A%20en%0Aday%3A%20%22Enter%20day%20number%22%0Ateaser_title%3A%20Evening%20Teaser%20–%20Day%20%0Ateaser_text%3A%20Highlights%20for%20the%20evening...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Or%20Monero%2FBTC%20address%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Support%20the%20author%20of%20this%20teaser%22%20%23%20Optional%0A%23%20Integrity%20hashes%20(automatically%20added%20after%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatically%20added%20after%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Evening%20Teaser%0A%0AHighlights%20for%20the%20evening..." 
         class="btn-contribute teaser">
        Add teaser
      </a>
    </div>
  </div>  
  
  
  {% comment %}
    Only English posts (lang: en)
  {% endcomment %}
  {% assign all_social_pages = site.pages | where: "lang", "en" | where_exp: "item", "item.path contains 'social-posts/'" %}
  {% assign rvn_only = all_social_pages | where_exp: "item", "item.path contains '-rvn'" %}
  {% assign teaser_only = all_social_pages | where_exp: "item", "item.path contains '-teaser'" %}

  {% assign social_posts = rvn_only | concat: teaser_only | uniq %}

  {% assign unique_days_raw = "" | split: "" %}
  {% assign seen = "" | split: "" %}

  {% for post in social_posts %}
    {% assign day_str = post.day | string | strip | default: "NO_DAY" %}
    {% unless seen contains day_str %}
      {% assign seen = seen | push: day_str %}
      {% assign unique_days_raw = unique_days_raw | push: day_str %}
    {% endunless %}
  {% endfor %}

  {% assign padded = "" | split: "" %}
  {% for d in unique_days_raw %}
    {% assign padded_d = d | prepend: "000" | slice: -3, 3 %}
    {% assign padded = padded | push: padded_d %}
  {% endfor %}

  {% assign padded = padded | sort_natural %}

  {% assign unique_days = "" | split: "" %}
  {% for p in padded %}
    {% assign orig = p | plus: 0 | string %}
    {% assign unique_days = unique_days | push: orig %}
  {% endfor %}

  {% for this_day in unique_days %}
    {% if this_day == "NO_DAY" or this_day == "" %}{% continue %}{% endif %}

    {% assign day_rvn    = nil %}
    {% assign day_teaser = nil %}

    {% assign this_day_str = this_day | string | strip %}

    {% for post in social_posts %}
      {% assign post_day_str = post.day | string | strip %}
      {% if post_day_str == this_day_str %}
        {% if post.path contains '-rvn' %}
          {% assign day_rvn = post %}
        {% elsif post.path contains '-teaser' %}
          {% assign day_teaser = post %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% if day_rvn or day_teaser %}
      <div class="social-card">

        <div class="social-header">
          <span class="social-number">Day {{ this_day }}</span>
        </div>

        {% if day_rvn %}
          <div class="rvn-title">
            <a href="{{ day_rvn.url | relative_url }}" class="full-title-link">
              {{ day_rvn.rvn_title | default: day_rvn.title | append: " – Reality vs Narrative" }}
            </a>
          </div>

          <div class="rvn-teaser">
            {{ day_rvn.rvn_teaser | default: day_rvn.teaser_text | default: "Reality vs Narrative analysis of the day." | strip_html | truncatewords: 35 }}
          </div>
        {% else %}
          <div class="rvn-title rvn-missing">No RVN yet for day {{ this_day }}</div>
          <div class="rvn-teaser"></div>
        {% endif %}

        <div class="divider"></div>

        {% if day_teaser %}
          <div class="teaser-title">
            <a href="{{ day_teaser.url | relative_url }}" class="teaser-title-link">
              {{ day_teaser.teaser_title | default: "Evening Teaser – Day " }}
            </a>
          </div>

          <div class="teaser-preview">
            {{ day_teaser.teaser_text | default: "Evening teaser with the highlights..." | strip_html | truncatewords: 25 }}
          </div>
        {% else %}
          <div class="teaser-title"></div>
          <div class="teaser-preview teaser-missing">No teaser yet</div>
        {% endif %}

      </div>
    {% endif %}
  {% endfor %}

</div>