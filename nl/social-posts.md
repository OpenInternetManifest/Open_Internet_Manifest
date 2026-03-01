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

{% comment %}
  Alleen Nederlandse posts ophalen (lang: nl)
{% endcomment %}
{% assign all_social_pages = site.pages | where: "lang", "nl" | where_exp: "item", "item.path contains 'social-posts/'" %}
{% assign rvn_only = all_social_pages | where_exp: "item", "item.path contains '-rvn'" %}
{% assign teaser_only = all_social_pages | where_exp: "item", "item.path contains '-teaser'" %}

{% assign social_posts = rvn_only | concat: teaser_only | uniq %}

<div class="social-grid">

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
              {{ day_teaser.teaser_title | default: "Avondteaser – Dag "  }}
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