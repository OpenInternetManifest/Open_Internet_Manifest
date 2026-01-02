---
layout: default
title: Hash Verifier
lang: NL
permalink: /nl/hash-verifier/
---

<div class="hash-verifier">
  <h1>Hash Verifier</h1>
  <p>Plaats hier een tekst uit het Open Internet Manifest om te controleren of het authentiek is en bij welke thesis/guide/begrip het hoort.</p>

  <textarea id="input-text" placeholder="Plak hier de tekst uit het manifest..." rows="12"></textarea>
  <button id="verify-btn" class="verify-button">
  {% if page.lang == "EN" %}
    Verify
  {% else %}
    Verifieer
  {% endif %}
</button>

  <div id="result" class="result-box" style="display:none;"></div>
</div>

