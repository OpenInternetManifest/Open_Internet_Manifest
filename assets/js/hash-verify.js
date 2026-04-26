document.addEventListener('DOMContentLoaded', function() {

  // ==================== UNIFIED FUZZY CLEAN ====================
  function fuzzyClean(text) {
    if (!text || typeof text !== 'string') return '';

    let t = text.normalize('NFKC');

    // Emoji's + variation selectors volledig verwijderen
    t = t.replace(/[\uD83C-\uDBFF\uDC00-\uDFFF\u2600-\u27FF\uFE0F\u200D\u2B50\u231A\u23E9-\u23FA\u25AA\u25AB\u25FB-\u25FE\u2600-\u26FF\u2700-\u27BF\u2B05-\u2B07\u2934\u2935\u2B50\u3297\u3299\u3030\u303D\u00A9\u00AE\u2122\u2139\u2194-\u2199\u21A9\u21AA\u231A\u231B\u2328\u23CF\u23E9-\u23F3\u23F8-\u23FA\u24C2\u25AA\u25AB\u25B6\u25C0\u25FB-\u25FE\u2600-\u26FF\u2705\u270A-\u270D\u270F\u2712\u2714\u2716\u271D\u2721\u2728\u2733\u2734\u2744\u2747\u274C\u274E\u2753-\u2755\u2757\u2763\u2764\u2795-\u2797\u27A1\u27B0\u27BF\u2934\u2935\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55\u3030\u303D\u3297\u3299\u00A9\u00AE\u2122\u2139]+/g, '');

    // Markdown stripping
    t = t.replace(/\*\*(.*?)\*\*/gs, '$1');
    t = t.replace(/__(.*?)__/gs, '$1');
    t = t.replace(/\*(.*?)\*/gs, '$1');
    t = t.replace(/_(.*?)_/gs, '$1');

    t = t.replace(/^#{1,6}\s+/gm, '');
    t = t.replace(/^>\s*/gm, '');
    t = t.replace(/^\s*[-*+]\s+/gm, ' ');
    t = t.replace(/^\s*\d+\.\s+/gm, ' ');

    t = t.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
    t = t.replace(/!\[.*?\]\(.*?\)/g, '');
    t = t.replace(/`([^`]+)`/g, '$1');
    t = t.replace(/^-{3,}\s*$/gm, ' ');

    t = t.replace(/<[^>]+>/g, '');

    // Extra fixes
    t = t.replace(/\s*\(\s*dag\s*,\s*/gi, ' (dag ');
    t = t.replace(/\s+,\s+/g, ', ');

    // Selectieve colon cleanup
    const titleColons = /(narratief|realiteit|hoe werkt het|hoe zien we dit|de grote verbinding|de oim-boodschap|traumabinding|cognitive dissonance|identificatie|overheid en burgers|social media|relaties en sekten|politiek|dank dat je|lees zelf|check zelf|weiger mee te spelen|schokkends|en vooral|passiviteit)/gi;
    t = t.replace(new RegExp(`(${titleColons.source})\\s*:\\s*`, 'gi'), '$1 ');

    // URLs + colons
    t = t.replace(/https?:\/\//g, '___URL___');
    t = t.replace(/:/g, ' ');
    t = t.replace(/___URL___/g, 'https://');

    // Finale normalisatie
    t = t.replace(/\s+/g, ' ').trim().toLowerCase();

    return t;
  }

  // ==================== VERIFY BUTTON ====================
  var verifyBtn = document.getElementById('verify-btn');
  var userHashInput = document.getElementById('user-hash');
  var verifyFeedback = document.getElementById('verify-feedback');

  var officialHash = document.getElementById('official-fuzzy-hash') 
                   ? document.getElementById('official-fuzzy-hash').value.trim() 
                   : null;

  if (verifyBtn && userHashInput && verifyFeedback) {
    verifyBtn.addEventListener('click', function() {
      var userHash = userHashInput.value.trim().toLowerCase();

      if (!userHash) {
        showFeedback(verifyFeedback, 'Plak eerst je berekende SHA256 hash.', 'warning');
        return;
      }
      if (!officialHash) {
        showFeedback(verifyFeedback, 'Kan officiële fuzzy hash niet vinden.', 'error');
        return;
      }

      if (userHash === officialHash.toLowerCase()) {
        showFeedback(verifyFeedback, '100% MATCH! Deze pagina is 100% authentiek.', 'success');
      } else {
        showFeedback(verifyFeedback, 'Geen match.<br>Jouw hash: ' + userHash + '<br>Officieel: ' + officialHash, 'error');
      }
    });

    userHashInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') verifyBtn.click();
    });
  }

  // ==================== COPY BUTTON (repost buttons nu ook verwijderd) ====================
  var copyBtn = document.querySelector('.big-copy-btn');
  var copyFeedback = document.getElementById('copy-feedback');

  if (copyBtn && copyFeedback) {
    copyBtn.addEventListener('click', function() {
      try {
        var main = document.querySelector('.main-content') || document.querySelector('main') || document.body;
        var temp = document.createElement('div');
        temp.innerHTML = main.innerHTML;

        // ==================== VERWIJDER ALLE IRRELEVANTE DELEN ====================
        var selectors = [
          '.integrity-check', '.integrity-content', '.verify-section', '.hash-verifier',
          '.copy-container', '.copy-feedback', '#verify-feedback', '.verify-feedback',
          '.community-box', '.donation-section', '.donation-content',
          '.footer-nav', '.site-footer', '.site-footer-credits', '.page-footer',
          '.banner', '.overlay-text', '.home-container',
          '.language-buttons', '.language-selector',
          '.manifest-header', '.manifest-subtitle', '.intro-title', '.intro-text',
          '.thesis-navigation-arrows', '.nav-arrow',
          '.reactions', '.giscus', '#giscus', '.giscus-container', '.giscus-comments',
          '.giscus-comment', '.giscus-discussion', '[data-giscus]', '.giscus-frame',
          '.comments-section', '.comment-notice', '#comments', '.comments',
          // === REPOST / SHARE BUTTONS ===
          '.repost-buttons', '.repost-section', '.share-buttons', '.share-section',
          '.social-buttons', '.repost-container', '#repost-buttons', '.copy-repost',
          '.big-copy-btn', '.copy-btn', '.repost-options',
          'button', 'script', 'style', 'nav', 'footer', 'header', 'aside',
          '.generated-by', '.goatcounter', '.goatcounter-link'
        ];

        selectors.forEach(function(sel) {
          temp.querySelectorAll(sel).forEach(function(el) {
            el.remove();
          });
        });

        var rawText = temp.textContent.trim();

        // Gebruik exact dezelfde clean als de verifier
        var cleanText = fuzzyClean(rawText);

        navigator.clipboard.writeText(cleanText).then(function() {
          showFeedback(copyFeedback, '✅ Fuzzy tekst gekopieerd!<br>Plak in een SHA256 tool.', 'success');
          setTimeout(() => { copyFeedback.innerHTML = ''; }, 4000);
        }).catch(function() {
          alert('Copy mislukt. Hier is de fuzzy tekst:\n\n' + cleanText);
          showFeedback(copyFeedback, 'Copy mislukt – tekst staat in popup.', 'warning');
        });

      } catch (err) {
        console.error(err);
        showFeedback(copyFeedback, 'Copy mislukt.', 'error');
      }
    });
  }

  function showFeedback(el, msg, type) {
    el.innerHTML = msg;
    el.style.color = type === 'success' ? '#66ff66' : '#ff6666';
  }
});