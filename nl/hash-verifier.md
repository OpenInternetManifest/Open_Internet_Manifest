---
layout: default
title: Hash Verifier
lang: NL
permalink: /nl/hash-verifier/
---

<div class="hash-verifier">
  <h1>Hash Verifier</h1>
  <p>Paste here a text from the Open Internet Manifest to check if it is authentic and which thesis/guide/concept it belongs to.</p>

  <textarea id="input-text" placeholder="Paste the text from the manifest here..." rows="12"></textarea>
  <button id="verify-btn">Verify</button>

  <div id="result" class="result-box" style="display:none;"></div>
</div>

<script src="{{ site.baseurl }}/assets/js/hash-verifier.js"></script>