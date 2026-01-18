---
layout: default
title: Hash Verifier
lang: nl

---

<div class="hash-verifier">
  <h1>Hash Verifier</h1>
  
  <p>
    Wil je controleren of een social post (teaser, Realiteit vs Narratief of andere bijdrage) authentiek is en niet is aangepast?  
    Plak de volledige tekst hieronder in (inclusief eventuele voetnoot of disclaimer).  
    De verifier controleert de cryptografische hash en bevestigt of de tekst exact overeenkomt met de versie die is vastgelegd op openinternetmanifest.org.
  </p>

  <blockquote>
    “Een hash is digitaal zegelwas: breek je het, dan ziet iedereen het.”  
    — Ruben Berkhout, december 2025
  </blockquote>

  <p>
    <strong>Waarom dit bestaat:</strong>  
    Narratieven worden snel vervormd, woorden uit context gehaald of subtiel gewijzigd.  
    Hashes bieden een onveranderlijk digitaal zegel: breek je het, dan is het direct zichtbaar.  
    Dit helpt om de integriteit van bijdragen aan het Open Internet Manifest te beschermen.
  </p>

  <p>
    <strong>Coming soon:</strong> fuzzy matching!  
    Dan kun je ook posts met kleine variaties (typografische fouten, spaties, emoji-wissels) herkennen als “bijna exact hetzelfde”, zodat de herkomst nog steeds traceerbaar blijft.
  </p>

  <p>
    Het Open Internet Manifest is een community effort.  
    Elke post die hier wordt vastgelegd, kan door iedereen gecontroleerd worden.  
    Op termijn groeit dit uit tot een collectief archief van authentieke bijdragen — van iedereen die meedoet.
  </p>

  <p>
    Plak hier de volledige tekst uit een social post (teaser, Realiteit vs Narratief, etc.) om te controleren of hij authentiek is en bij welke thesis/guide/begrip hij hoort.
  </p>

  <textarea id="input-text" placeholder="Plak hier de volledige tekst uit de social post (incl. voetnoot/disclaimer)..." rows="12"></textarea>
  <button id="verify-btn" class="verify-button">
    {% if page.lang == "EN" %}
      Verify
    {% else %}
      Verifieer
    {% endif %}
  </button>

  <div id="result" class="result-box" style="display:none;"></div>
</div>
