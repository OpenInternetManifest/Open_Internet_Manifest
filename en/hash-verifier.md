---
layout: default
title: Hash Verifier
lang: EN
permalink: /en/hash-verifier/
---

<div class="hash-verifier">
  <h1>Hash Verifier</h1>
  <p>Paste here a text from the Open Internet Manifest to check if it is authentic and which thesis/guide/concept it belongs to.</p>

  <textarea id="input-text" placeholder="Paste the text from the manifest here..." rows="12"></textarea>
  <button id="verify-btn" class="verify-button">
  {% if page.lang == "EN" %}
    Verify
  {% else %}
    Verifieer
  {% endif %}
</button>

  <div id="result" class="result-box" style="display:none;"></div>
</div>

<!-- Centrale hashes + verifier JS -->
<script src="{{ site.baseurl }}/assets/js/official-hashes.js"></script>
<script src="{{ site.baseurl }}/assets/js/hash-verifier.js"></script>