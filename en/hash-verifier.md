---
layout: default
title: Hash Verifier
lang: EN

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
  
