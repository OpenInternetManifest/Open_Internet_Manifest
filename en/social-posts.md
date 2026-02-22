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

  {% assign posts = site.pages | where_exp: "p", "p.dir == '/en/social-posts/'" | sort: "day" %}

  {% if posts.size > 0 %}
    {% for post in posts %}
      {% if post.url != page.url and post.day %}
        <div class="social-card">
          <div class="social-header">
            <span class="social-number">Day {{ post.day }}</span>
            <h3>
              <a href="{{ post.rvn_url | relative_url }}">RVN: {{ post.rvn_title | default: post.title }}</a>
            </h3>
          </div>
          
          <p class="social-teaser">
            {{ post.rvn_teaser | default: "Reality vs Narrative analysis of the day." }}
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
      (debug) No social posts found.
    </p>
  {% endif %}

</div>