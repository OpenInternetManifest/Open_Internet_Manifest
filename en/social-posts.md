---
layout: default
lang: en
title: Reality vs Narrative – Social Posts
---

<div class="social-hero">
  <h1 class="intro-title">Reality vs Narrative</h1>
  
  <h2 class="manifest-subtitle">
    Daily confrontation between what we are told and what actually happens.
  </h2>
  
  <p class="intro-text">
    Every day a teaser (evening) and a full RVN analysis (morning) — follow day by day or dive into a specific moment.
  </p>
</div>

<div class="social-grid">
  {% comment %}
    Groepeer per dag: 1 card per dag met RVN + Teaser (als beide bestaan)
    Sorteer op 'day' uit frontmatter
  {% endcomment %}

  {% assign social_posts = site.pages | where_exp: "p", "p.path contains '/social-posts/'" | where_exp: "p", "p.path contains '-rvn' or p.path contains '-teaser'" | sort: "day" %}

  {% assign processed_days = "" | split: "" %}

  {% for post in social_posts %}
    {% assign this_day = post.day %}

    {% assign already_processed = false %}
    {% for pd in processed_days %}
      {% if pd == this_day %}
        {% assign already_processed = true %}
      {% endif %}
    {% endfor %}
    {% if already_processed %}
      {% continue %}
    {% endif %}

    {% assign processed_days = processed_days | push: this_day %}

    {% assign day_rvn = nil %}
    {% assign day_teaser = nil %}

    {% for p in social_posts %}
      {% if p.day == this_day %}
        {% if p.path contains '-rvn' %}
          {% assign day_rvn = p %}
        {% elsif p.path contains '-teaser' %}
          {% assign day_teaser = p %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% if day_rvn or day_teaser %}
      <div class="social-card">
        <div class="social-header">
          <span class="social-number">Day {{ this_day }}</span>
        </div>
        
        {% if day_rvn %}
  <h3>
    <a href="{{ day_rvn.url | relative_url }}" class="full-title-link">
      RVN: {{ day_rvn.rvn_title | default: day_rvn.title  }}
    </a>
  </h3>
  <div class="rvn-content">
  <p class="social-teaser">
    {{ day_rvn.rvn_teaser | default: day_rvn.teaser_text | default: "Reality vs Narrative analyse van de dag." | truncate: 120 }}
  </p>
</div>
<div class="divider"></div>  <!-- altijd tonen, vaste positie -->
{% endif %}

{% if day_teaser %}
  <div class="teaser-preview">
    <strong>
      <a href="{{ day_teaser.url | relative_url }}">
        {{ day_teaser.teaser_title | default: day_teaser.title }}
      </a>
    </strong><br>
    <small>
      {{ default: "Teaser dag " | default: day_teaser.title | truncate: 80 }}
    </small>
  </div>
{% endif %}
      </div>
    {% endif %}
  {% endfor %}

  {% if social_posts.size == 0 %}
    <p style="color: #f66; text-align:center; padding: 3rem;">
      (debug) No social posts found.
    </p>
  {% endif %}
</div>