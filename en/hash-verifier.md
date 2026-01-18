---
layout: default
title: Hash Verifier
lang: en

---

<div class="hash-verifier">
  <h1>Hash Verifier</h1>
  
  <p>
    Want to check if a social post (teaser, Reality vs Narrative, or other contribution) is authentic and hasn’t been altered?  
    Paste the full text below (including any footnote or disclaimer).  
    The verifier checks the cryptographic hash and confirms whether it exactly matches the version archived on openinternetmanifest.org.
  </p>

  <blockquote>
    “A hash is digital sealing wax: break it, and everyone sees it.”  
    — Ruben Berkhout, December 2025
  </blockquote>

  <p>
    <strong>Why this exists:</strong>  
    Narratives are easily distorted, words taken out of context, or subtly changed.  
    Hashes provide an immutable digital seal: break it, and the change is immediately visible.  
    This helps protect the integrity of contributions to the Open Internet Manifest.
  </p>

  <p>
    <strong>Coming soon:</strong> fuzzy matching!  
    Soon you’ll be able to recognize posts with minor variations (typos, spacing changes, emoji swaps) as “nearly exact”, keeping the origin traceable.
  </p>

  <p>
    The Open Internet Manifest is a community effort.  
    Every post archived here can be verified by anyone.  
    Over time, this will grow into a collective archive of authentic contributions — from everyone who participates.
  </p>

  <p>
    Paste the full text from a social post (teaser, Reality vs Narrative, etc.) here to verify if it’s authentic and which thesis/guide/concept it belongs to.
  </p>

  <textarea id="input-text" placeholder="Paste the full text from the social post here (incl. footnote/disclaimer)..." rows="12"></textarea>
  <button id="verify-btn" class="verify-button">
    {% if page.lang == "EN" %}
      Verify
    {% else %}
      Verifier
    {% endif %}
  </button>

  <div id="result" class="result-box" style="display:none;"></div>
</div>