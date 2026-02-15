---
layout: default
lang: en
title: All Guides
---

<div class="guides-hero">
  <h1 class="intro-title">Practical Guides</h1>
  
  <h2 class="manifest-subtitle">
    Concrete steps to break free from Big Tech and take back ownership of your communication and data.
  </h2>
  
  <p class="intro-text">
    From simple account creation to running your own server — start wherever you are.
  </p>
</div>

<div class="guides-grid">

  {% assign guide_pages = site.pages | where_exp: "p", "p.dir == '/en/guides/'" | sort: "order" %}

  {% for guide in guide_pages %}
    {% if guide.url != page.url and guide.title and guide.title != "" %}
      <a href="{{ guide.url | relative_url }}" class="guide-card" data-difficulty="{{ guide.difficulty | default: 'beginner' }}">
        <div class="guide-header">
          <span class="guide-number">{{ forloop.index }}</span>
          <h3>{{ guide.title }}</h3>
        </div>
        <p class="guide-teaser">{{ guide.teaser | default: "Practical step-by-step guide." }}</p>
        
        <span class="difficulty-banner {{ guide.difficulty | default: 'beginner' }}">
          {% case guide.difficulty %}
            {% when 'beginner' %}Beginner
            {% when 'intermediate' %}Intermediate
            {% when 'advanced' %}Advanced
            {% else %}Beginner
          {% endcase %}
        </span>
        
        <span class="read-more">Read the guide →</span>
      </a>
    {% endif %}
  {% endfor %}

  {% if guide_pages.size == 0 or guide_pages.size == 1 %}
    <p style="color: #f66; text-align:center;">(debug) No guides found or only this overview page itself.</p>
  {% endif %}

</div>