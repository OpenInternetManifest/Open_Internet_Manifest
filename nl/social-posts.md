---
layout: default
lang: nl
title: Realiteit vs Narratief – Social Posts
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

  <!-- Unified add-card via include -->
  {% assign now_date = 'now' | date: '%Y-%m-%d' %}

  {% assign rvn_template_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/nl?filename=" | append: now_date | append: "-rvn-dag.md&value=---%0Alang%3A%20nl%0Aday%3A%20%22Vul%20dagnummer%20in%22%0Arvn_title%3A%20Realiteit%20vs%20Narratief%0Arvn_teaser%3A%20Korte%20inhoud%20voor%20de%20RVN...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Steun%20de%20auteur%20van%20deze%20RVN%22%20%23%20Optioneel%0A%23%20Integrity%20hashes%20(automatisch%20toegevoegd%20na%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatisch%20toegevoegd%20na%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Realiteit%0A%0A...%0A%0A## Narratief%0A%0A...%0A%0A## Analyse%0A%0A..." %}

  {% assign teaser_template_url = "https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/nl?filename=" | append: now_date | append: "-teaser-dag.md&value=---%0Alang%3A%20nl%0Aday%3A%20%22Vul%20dagnummer%20in%22%0Ateaser_title%3A%20Avondteaser%20–%20Dag%20%0Ateaser_text%3A%20Hoogtepunten%20voor%20de%20avond...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fexample-link%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Steun%20de%20auteur%20van%20deze%20teaser%22%20%23%20Optioneel%0A%23%20Integrity%20hashes%20(automatisch%20toegevoegd%20na%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatisch%20toegevoegd%20na%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Avondteaser%0A%0AHoogtepunten%20voor%20de%20avond..." %}

  {% capture add_extra_content %}
    <div class="rvn-title">Schrijf een nieuwe RVN-dag in NL, EN of andere taal. Straks via /admin/, nu via GitHub PR.</div>
    
    <div class="contribute-buttons rvn">
      <a href="{{ rvn_template_url }}" class="btn-contribute rvn">Voeg RVN toe</a>
    </div>
    
    <div class="divider"></div>
    
    <div class="teaser-title">Avondteaser – Dag</div>
    
    <div class="contribute-buttons teaser">
      <a href="{{ teaser_template_url }}" class="btn-contribute teaser">Voeg teaser toe</a>
    </div>
  {% endcapture %}

  {% include card.html 
    type="contribution" 
    url="#" 
    title="Voeg nieuwe RVN / Teaser dag toe" 
    teaser="" 
    extra_class="contribution-card social-card" 
    extra_content=add_extra_content 
  %}

  {% comment %}
    Alleen Nederlandse posts (lang: nl)
  {% endcomment %}
 {% assign all_social_pages = site.pages | where: "lang", "nl" | where_exp: "item", "item.path contains 'social-posts/'" %}
{% assign rvn_only = all_social_pages | where_exp: "item", "item.path contains '-rvn'" %}
{% assign teaser_only = all_social_pages | where_exp: "item", "item.path contains '-teaser'" %}
  {% assign social_posts = rvn_only | concat: teaser_only | uniq %}

  {% assign unique_days_raw = "" | split: "" %}
  {% assign seen = "" | split: "" %}

  {% for post in social_posts %}
    {% assign day_str = post.day | default: "" | strip %}
    {% unless day_str == "" or seen contains day_str %}
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
    {% if this_day == "" %}{% continue %}{% endif %}

    {% assign day_rvn    = nil %}
    {% assign day_teaser = nil %}

    {% assign this_day_str = this_day | strip %}

    {% for post in social_posts %}
      {% assign post_day_str = post.day | default: "" | strip %}
      {% if post_day_str == this_day_str %}
        {% if post.path contains "-rvn" %}
          {% assign day_rvn = post %}
        {% elsif post.path contains "-teaser" %}
          {% assign day_teaser = post %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% if day_rvn or day_teaser %}
      <div class="social-card">

        <div class="card-header-light">
          <span class="card-number">Dag {{ this_day }}</span>
        </div>

        {% if day_rvn %}
          <div class="rvn-title">
            <a href="{{ day_rvn.url | relative_url }}">
              {{ day_rvn.rvn_title | default: day_rvn.title | append: " – Realiteit vs Narratief" }}
            </a>
          </div>

          <div class="rvn-teaser">
            {{ day_rvn.rvn_teaser | default: day_rvn.teaser_text | default: "Realiteit vs Narratief analyse van de dag." | strip_html | truncatewords: 35 }}
          </div>
        {% else %}
          <div class="rvn-title rvn-missing">Nog geen RVN voor dag {{ this_day }}</div>
          <div class="rvn-teaser"></div>
        {% endif %}

        <div class="divider"></div>

        {% if day_teaser %}
          <div class="teaser-title">
            <a href="{{ day_teaser.url | relative_url }}">
              {{ day_teaser.teaser_title | default: "Avondteaser – Dag " | append: this_day }}
            </a>
          </div>

          <div class="teaser-preview">
            {{ day_teaser.teaser_text | default: "Avondteaser met de hoogtepunten..." | strip_html | truncatewords: 25 }}
          </div>
        {% else %}
          <div class="teaser-title"></div>
          <div class="teaser-preview teaser-missing">Nog geen teaser</div>
        {% endif %}

      </div>
    {% endif %}
  {% endfor %}

</div>