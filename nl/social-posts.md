---
layout: default
lang: nl
title: Realiteit vs Narratief – Social Posts
---

<div class="social-posts-hero">
  <h1 class="intro-title">Realiteit vs Narratief</h1>
  
  <h2 class="manifest-subtitle">
    Dagelijkse confrontatie tussen wat ons verteld wordt en wat er werkelijk gebeurt.
  </h2>
  
  <p class="intro-text">
    Elke dag een teaser ('s avonds) en een volledige RVN-analyse ('s ochtends) — volg dag voor dag of duik in een specifiek moment.
  </p>
</div>

<div class="social-grid">

  <!-- + Bijdrage toevoegen als eerste card – exacte grid-match met normale cards -->
  <div class="social-card contribution-card">
    <div class="social-header">
      <span class="social-number">+</span>
    </div>

    <!-- RVN titel placeholder -->
    <div class="rvn-title">
      Realiteit vs Narratief
    </div>

    <!-- RVN teaser / beschrijving -->
    <div class="rvn-teaser">
      Schrijf een nieuwe RVN-dag + teaser – in NL, EN of andere taal.<br>
      Straks via /admin/, nu via GitHub PR.
    </div>

    <!-- Button RVN – boven divider -->
    <div class="contribute-buttons rvn">
      <a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/nl?filename={{ 'now' | date: '%Y-%m-%d' }}-rvn-dag.md&value=---%0Alang%3A%20nl%0Aday%3A%20%22Vul%20dag%20nummer%20in%22%0Arvn_title%3A%20Realiteit%20vs%20Narratief%0Arvn_teaser%3A%20Korte%20inhoud%20voor%20de%20RVN...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fvoorbeeldlink%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Ondersteun%20de%20auteur%20van%20deze%20RVN%22%20%23%20Optioneel%0A%23%20Integriteit%20hashes%20(automatisch%20toegevoegd%20na%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatisch%20toegevoegd%20na%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Realiteit%0A%0A...%0A%0A## Narratief%0A%0A...%0A%0A## Analyse%0A%0A..." 
         class="btn-contribute rvn">
        Voeg RVN toe
      </a>
    </div>

    <!-- Divider -->
    <div class="divider"></div>

    <!-- Teaser titel placeholder -->
    <div class="teaser-title">
      Avondteaser – Dag
    </div>

    <!-- Teaser preview placeholder -->
    <div class="teaser-preview">
      Hoogtepunten voor de avond...
    </div>

    <!-- Button teaser – onder divider -->
    <div class="contribute-buttons teaser">
      <a href="https://github.com/OpenInternetManifest/Open_Internet_Manifest/new/main/_social-posts/nl?filename={{ 'now' | date: '%Y-%m-%d' }}-teaser-dag.md&value=---%0Alang%3A%20nl%0Aday%3A%20%22Vul%20dag%20nummer%20in%22%0Ateaser_title%3A%20Avondteaser%20–%20Dag%20%0Ateaser_text%3A%20Hoogtepunten%20voor%20de%20avond...%0A%23%20donation_link%3A%20%22https%3A%2F%2Fbuy.stripe.com%2Fvoorbeeldlink%22%20%23%20Of%20Monero%2FBTC%20adres%2C%20Ko-fi%2C%20etc.%0A%23%20donation_text%3A%20%22Ondersteun%20de%20auteur%20van%20deze%20teaser%22%20%23%20Optioneel%0A%23%20Integriteit%20hashes%20(automatisch%20toegevoegd%20na%20merge)%0Awebsite_sha256%3A%20%27%27%0Asocial_x_sha256%3A%20%27%27%0Asocial_fb_sha256%3A%20%27%27%0Asocial_share_sha256%3A%20%27%27%0A%23%20Git%20commit%20info%20(automatisch%20toegevoegd%20na%20merge)%0Agit_commit_hash%3A%20%27%27%0Agit_commit_url%3A%20%27%27%0A---%0A%0A## Avondteaser%0A%0AHoogtepunten%20voor%20de%20avond..." 
         class="btn-contribute teaser">
        Voeg teaser toe
      </a>
    </div>
  </div>

  <!-- Bestaande loop – laat intact -->
  {% comment %}
    Alleen Nederlandse posts ophalen (lang: nl)
  {% endcomment %}
  {% assign all_social_pages = site.pages | where: "lang", "nl" | where_exp: "item", "item.path contains 'social-posts/'" %}
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
          <span class="social-number">Dag {{ this_day }}</span>
        </div>

        {% if day_rvn %}
          <div class="rvn-title">
            <a href="{{ day_rvn.url | relative_url }}" class="full-title-link">
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
            <a href="{{ day_teaser.url | relative_url }}" class="teaser-title-link">
              {{ day_teaser.teaser_title | default: "Avondteaser – Dag " }}
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