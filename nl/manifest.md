---
layout: default
lang: nl
title: Alle Theses
---

<div class="theses-hero">
  <h1 class="intro-title">De eerste 30 theses zijn klaar</h1>
  
  <h2 class="manifest-subtitle">
    Dit manifest leeft — het groeit door bijdragen van mensen zoals jij.
  </h2>
  
  <p class="intro-text">
    100 theses voor een vrij, open en onvervreemdbaar internet. Begin waar je wilt — of lees vanaf het begin.
  </p>
</div>

<div class="theses-grid">

  {% assign all_pages_in_theses = site.pages | where_exp: "p", "p.dir == '/nl/theses/'" | sort: "order" %}

  {% assign theses_nl = all_pages_in_theses | where: "lang", "nl" %}

  {% if theses_nl.size > 0 %}
    {% for thesis in theses_nl %}
      {% if thesis.url != page.url %}  <!-- sluit de manifest-pagina zelf uit -->
        <a href="{{ thesis.url | relative_url }}" class="thesis-card">
          <div class="thesis-header">
            <span class="thesis-number">{{ forloop.index }}</span>
            <h3>{{ thesis.title }}</h3>
          </div>
          <p class="thesis-teaser">{{ thesis.teaser | default: "Lees de volledige these." }}</p>
          
          <!-- Progress label rechtsboven -->
          <span class="thesis-progress">Thesis {{ forloop.index }}/30</span>
          
          <span class="read-more">Lees volledig →</span>
        </a>
      {% endif %}
    {% endfor %}
  {% else %}
    <p style="color: #f66; text-align:center; padding: 2rem;">
      (debug) Geen theses gevonden in /nl/theses/.<br>
      Controleer: bestaan de bestanden? Hebben ze front matter met order: en lang: nl?
    </p>
  {% endif %}

</div>