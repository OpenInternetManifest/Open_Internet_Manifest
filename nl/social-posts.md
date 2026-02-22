---
layout: default
lang: nl
title: Reality vs Narrative – Social Posts
---

<div class="social-hero">
  <h1 class="intro-title">Reality vs Narrative</h1>
  
  <h2 class="manifest-subtitle">
    Dagelijkse confrontatie tussen wat ons verteld wordt en wat er werkelijk gebeurt.
  </h2>
  
  <p class="intro-text">
    Elke dag een teaser (avond) en een volledige RVN-analyse (ochtend) — volg het dag voor dag of duik in een specifiek moment.
  </p>
</div>

<div class="social-grid">

  {% assign posts = site.pages | where_exp: "p", "p.dir == '/nl/social-posts/'" | sort: "day" %}

  {% if posts.size > 0 %}
    {% for post in posts %}
      {% if post.url != page.url and post.day %}
        <div class="social-card">
          <div class="social-header">
            <span class="social-number">Dag {{ post.day }}</span>
            <h3>
              <a href="{{ post.rvn_url | relative_url }}">RVN: {{ post.rvn_title | default: post.title }}</a>
            </h3>
          </div>
          
          <p class="social-teaser">
            {{ post.rvn_teaser | default: "Reality vs Narrative analyse van de dag." }}
          </p>
          
          {% if post.teaser_title %}
            <div class="teaser-preview">
              <strong>Teaser: <a href="{{ post.teaser_url | relative_url }}">{{ post.teaser_title }}</a></strong><br>
              <small>
                {{ post.teaser_text | default: post.teaser_title | truncate: 80 }}
              </small>
            </div>
          {% endif %}
        </div>
      {% endif %}
    {% endfor %}
  {% else %}
    <p style="color: #f66; text-align:center; padding: 3rem;">
      (debug) Geen social-posts gevonden.
    </p>
  {% endif %}

</div>