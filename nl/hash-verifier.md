---
layout: default
title: Hash Verifier
lang: nl
---

<div class="hash-verifier">

  <h1>Hash Verifier</h1>

  <p class="intro">
    Controleer zelf of een post van het Open Internet Manifest authentiek is.<br>
    Plak de volledige tekst hieronder (inclusief eventuele voetnoot of hashtags) en klik op Verifieer.
  </p>

    <!-- Prominente quote - cleaner versie -->
  <div class="highlight-quote">
    <blockquote>
      “Een hash is digitaal zegelwas:<br>
      <span class="quote-highlight">breek je het, dan ziet iedereen het.</span>”
    </blockquote>
    <cite>— Ruben Berkhout, december 2025</cite>
  </div>

  <div class="section">
    <strong>Waarom dit bestaat</strong>
    <p>
      Narratieven worden dagelijks verdraaid, woorden uit context gehaald of subtiel aangepast. 
      Daarom gebruiken we hashes: een digitaal zegel dat laat zien of een tekst nog origineel is.
    </p>
  </div>

    <div class="section">
    <strong>Wat is een "fuzzy hash"?</strong>
    
    <p>
      Normale hashes zijn extreem streng: één spatie, één emoji of één vetgedrukt woord en de hash is al anders.
    </p>
    
    <p>
      Omdat posts vaak worden gedeeld via X, Facebook, Telegram, e-mail of kopieer-plak acties, 
      veranderen kleine dingen (extra spaties, nieuwe regels, vetgedrukte woorden, etc.).
    </p>
    
    <p>
      Daarom gebruiken wij een <em>fuzzy hash</em>: een slimme, vergevingsgezinde hash die kleine 
      opmaak- en formaatverschillen negeert, maar de echte inhoud wel beschermt. 
      Zo blijft een post herkenbaar als authentiek, zelfs nadat hij meerdere keren 
      is gedeeld of licht is aangepast.
    </p>
  </div>

  <p class="instruction">
    Plak hier de volledige tekst van een social post, teaser of andere bijdrage:
  </p>

  {% include fuzzy-hashes.html %}

  <textarea id="input-text" 
            placeholder="Plak hier de volledige tekst (incl. voetnoot, hashtags of disclaimer)..." 
            rows="14"></textarea>

  <button id="verify-btn" class="verify-button">
    Verifieer
  </button>

  <div id="result" class="result-box" style="display:none;"></div>

</div>

<script src="{{ '/assets/js/hash-verifier.js' | relative_url }}"></script>