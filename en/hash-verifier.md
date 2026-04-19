---
layout: default
title: Hash Verifier
lang: en
---

<div class="hash-verifier">

  <h1>Hash Verifier</h1>

  <p class="intro">
    Check for yourself whether a post from the Open Internet Manifest is authentic.<br>
    Paste the full text below (including any footnote or hashtags) and click Verify.
  </p>

  <!-- Prominente quote - cleaner versie -->
  <div class="highlight-quote">
    <blockquote>
      “A hash is digital sealing wax:<br>
      <span class="quote-highlight">break it, and everyone will see it.</span>”
    </blockquote>
    <cite>— Ruben Berkhout, December 2025</cite>
  </div>

  <div class="section">
    <strong>Why this exists</strong>
    <p>
      Narratives are distorted daily, words are taken out of context or subtly altered. 
      That’s why we use hashes: a digital seal that shows whether a text is still the original version.
    </p>
  </div>

  <div class="section">
    <strong>What is a "fuzzy hash"?</strong>
    
    <p>
      Normal hashes are extremely strict: one space, one emoji or one bold word and the hash is already different.
    </p>
    
    <p>
      Because posts are often shared via X, Facebook, Telegram, email or copy-paste actions, 
      small things change (extra spaces, new lines, bold words, etc.).
    </p>
    
    <p>
      That’s why we use a <em>fuzzy hash</em>: a smart, forgiving hash that ignores minor formatting 
      and layout differences, but still protects the real content. 
      This way a post remains recognisable as authentic, even after being shared multiple times or slightly modified.
    </p>
  </div>

  <p class="instruction">
    Paste the full text of a social post, teaser or other contribution here:
  </p>

  {% include fuzzy-hashes.html %}

  <textarea id="input-text" 
            placeholder="Paste the full text here (incl. footnote, hashtags or disclaimer)..." 
            rows="14"></textarea>

  <button id="verify-btn" class="verify-button">
    Verify
  </button>

  <div id="result" class="result-box" style="display:none;"></div>

</div>

<script src="{{ '/assets/js/hash-verifier.js' | relative_url }}"></script>