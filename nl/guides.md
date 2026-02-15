---
layout: default
lang: nl
title: Alle Guides
---

<div class="guides-hero">
  <h1 class="intro-title">Praktische handleidingen</h1>
  
  <h2 class="manifest-subtitle">
    Concrete stappen om te ontsnappen aan Big Tech en weer eigenaar te worden van je communicatie en data.
  </h2>
  
  <p class="intro-text">
    Van simpele account-aanmaak tot het draaien van je eigen server — begin waar je staat.
  </p>
</div>

<div class="guides-grid">

  {% assign guide_pages = site.pages | where_exp: "p", "p.dir == '/nl/guides/'" | sort: "order" %}

  {% for guide in guide_pages %}
    {% if guide.url != page.url and guide.title and guide.title != "" %}
      <a href="{{ guide.url | relative_url }}" class="guide-card" data-difficulty="{{ guide.difficulty | default: 'beginner' }}">
        <div class="guide-header">
          <span class="guide-number">{{ forloop.index }}</span>
          <h3>{{ guide.title }}</h3>
        </div>
        <p class="guide-teaser">{{ guide.teaser | default: "Praktische stap-voor-stap handleiding." }}</p>
        
        <span class="difficulty-banner {{ guide.difficulty | default: 'beginner' }}">
          {% case guide.difficulty %}
            {% when 'beginner' %}Beginner
            {% when 'gemiddeld' %}Gemiddeld
            {% when 'gevorderd' %}Gevorderd
            {% else %}Beginner
          {% endcase %}
        </span>
        
        <span class="read-more">Lees de guide →</span>
      </a>
    {% endif %}
  {% endfor %}

  {% if guide_pages.size == 0 or guide_pages.size == 1 %}
    <p style="color: #f66; text-align:center;">(debug) Geen guides gevonden of alleen deze overzichtspagina zelf.</p>
  {% endif %}

</div>