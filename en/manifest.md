---
layout: default
lang: en
title: All Theses
---

<div class="theses-hero">
  <h1 class="intro-title">The first 30 theses are ready</h1>
  
  <h2 class="manifest-subtitle">
    This manifesto is alive — it grows through contributions from people like you.
  </h2>
  
  <p class="intro-text">
    100 theses for a free, open and unalienable internet. Start anywhere — or read from the beginning.
  </p>
</div>

<div class="theses-grid">

  {% assign all_pages_in_theses = site.pages | where_exp: "p", "p.dir == '/en/theses/'" | sort: "order" %}

  {% assign theses_en = all_pages_in_theses | where: "lang", "en" %}

  {% if theses_en.size > 0 %}
    {% for thesis in theses_en %}
      {% if thesis.url != page.url %}  <!-- exclude this manifest page itself -->
        <a href="{{ thesis.url | relative_url }}" class="thesis-card">
          <div class="thesis-header">
            <span class="thesis-number">{{ forloop.index }}</span>
            <h3>{{ thesis.title }}</h3>
          </div>
          <p class="thesis-teaser">{{ thesis.teaser | default: "Read the full thesis." }}</p>
          
          <!-- Progress label top-right -->
          <span class="thesis-progress">Thesis {{ forloop.index }}/30</span>
          
          <span class="read-more">Read full →</span>
        </a>
      {% endif %}
    {% endfor %}
  {% else %}
    <p style="color: #f66; text-align:center; padding: 2rem;">
      (debug) No theses found in /en/theses/.<br>
      Check: do the files exist? Do they have front matter with order: and lang: en?
    </p>
  {% endif %}

</div>