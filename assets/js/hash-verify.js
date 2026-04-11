window.copyPageText = function() {
  const mainContent = document.querySelector('.main-content') || document.querySelector('main') || document.querySelector('article');
  if (!mainContent) {
    showFeedback('copy-feedback', false, '❌ Kan hoofdinhoud niet vinden');
    return;
  }

  const clone = mainContent.cloneNode(true);

  // Verwijder ongewenste elementen
  const unwanted = [
    '.integrity-check', '.integrity-content', '.verify-section', '.hash-verifier',
    '.copy-container', '.copy-feedback', '#verify-feedback', '.verify-feedback',
    '.community-box', '.donation-section',
    '.footer-nav', '.site-footer', '.site-footer-credits', '.page-footer',
    '.banner', '.overlay-text',
    '.home-container', '.language-buttons', '.language-selector',
    '.manifest-header', '.manifest-subtitle', '.intro-title', '.intro-text',
    '.thesis-navigation-arrows', '.nav-arrow',
    'button', 'script', 'code', 'nav', 'footer', 'header',
    '.comments-section', '.comment-notice', '#giscus', '.giscus', 'giscus-widget',
    '.giscus-container', '.giscus-comments', '.giscus-comment', '.giscus-discussion',
    '[data-giscus]', '.comments', '#comments', '.giscus-frame', '.giscus-loading'
  ];

  clone.querySelectorAll(unwanted.join(', ')).forEach(el => el.remove());

  // Extra Giscus cleanup
  clone.querySelectorAll('iframe[src*="giscus"], div[class*="giscus"], div[id*="giscus"]').forEach(el => el.remove());

  // Verwijder "Reacties" headings
  clone.querySelectorAll('h2, h3').forEach(el => {
    const txt = el.textContent.trim().toLowerCase();
    if (txt.includes('reactie') || txt.includes('comment') || txt.includes('reageren')) {
      el.remove();
    }
  });

  // Verwijder hash-verificatie uitleg (laat footer staan)
  clone.querySelectorAll('p').forEach(p => {
    const text = p.textContent.trim().toLowerCase();
    if (text.includes('hash verificatie') || text.includes('wat is nu eigenlijk hash') || text.includes('sha256 verifier')) {
      p.remove();
    }
  });

  let text = clone.innerText || clone.textContent || '';

  // Zeer milde cleanup
  text = text
    .replace(/\r\n/g, '\n')
    .replace(/\n{5,}/g, '\n\n\n\n')   // max 4 newlines
    .replace(/[ \t]+/g, ' ')
    .trim();

  // Per regel trimmen
  text = text
    .split('\n')
    .map(line => line.trim())
    .join('\n');

  // Verwijder extra lege regel na ":" (zowel bij "via:" als bij opsomming)
  text = text.replace(/:[ \t]*\n\n/g, ':\n');

  // Verwijder extra lege regel na opsomming (na laatste item)
  text = text.replace(/\n\n\n+/g, '\n\n');

  navigator.clipboard.writeText(text).then(() => {
    showFeedback('copy-feedback', true, '✓ Pagina tekst gekopieerd!<br>Plak in SHA-256 tool → moet matchen met website_sha256');
  }).catch(() => {
    showFeedback('copy-feedback', false);
  });
};

window.verifyHash = function() {
  const userHash = document.getElementById('user-hash')?.value.trim().toLowerCase();
  const feedback = document.getElementById('verify-feedback');
  if (!feedback) return;

  if (!userHash) {
    showFeedback('verify-feedback', false, '✗ Voer een hash in');
    return;
  }

  // Haal de officiële hash op uit data-attribuut op <body> of <main>
  const pageHash = document.documentElement.dataset.websiteSha256 || 
                   document.body.dataset.websiteSha256 || 
                   null;

  const lang = document.documentElement.lang || 'nl';

  if (!pageHash) {
    showFeedback('verify-feedback', false, '❌ Geen officiële hash gevonden op deze pagina.');
    return;
  }

  if (userHash === pageHash.toLowerCase()) {
    const matchText = lang === 'en' ? '✓ PERFECTE MATCH!' : '✓ PERFECTE MATCH!';
    const authText = lang === 'en' ? 'Deze pagina is 100% authentiek.' : 'Deze pagina is 100% authentiek.';
    feedback.innerHTML = `<span style="color: #66ff66 !important; font-size: 1.2em; font-weight: bold;">${matchText}</span><br>${authText}`;
  } else {
    const noMatch = lang === 'en' ? '✗ Geen match' : '✗ Geen match';
    const your = lang === 'en' ? 'Jouw hash:' : 'Jouw hash:';
    const official = lang === 'en' ? 'Officiële hash:' : 'Officiële hash:';
    feedback.innerHTML = `<span style="color: #ff6666 !important; font-weight: bold;">${noMatch}</span><br>
      <strong>${your}</strong> <code style="word-break: break-all;">${userHash}</code><br>
      <strong>${official}</strong> <code style="word-break: break-all;">${pageHash}</code>`;
  }
};

function showFeedback(id, success, custom = null) {
  const el = document.getElementById(id);
  if (!el) return;

  let html = '';

  if (custom) {
    // Custom berichten (zoals copy succes met uitleg) → altijd groen
    html = `<span style="color: #66ff66 !important; font-weight: bold;">${custom}</span>`;
  } else if (success) {
    // Standaard succes (bijv. copy zonder custom)
    const lang = document.documentElement.lang || 'nl';
    const text = lang === 'en' ? '✓ Pagina tekst gekopieerd!' : '✓ Pagina tekst gekopieerd!';
    html = `<span style="color: #66ff66 !important; font-weight: bold;">${text}</span>`;
  } else {
    // Foutmeldingen → rood
    const lang = document.documentElement.lang || 'nl';
    const text = lang === 'en' ? 'Copy mislukt – selecteer handmatig' : 'Copy mislukt – selecteer handmatig';
    html = `<span style="color: #ff6666 !important;">${text}</span>`;
  }

  el.innerHTML = html;

  // Verberg na 4 seconden bij succes
  if (success) {
    setTimeout(() => { el.innerHTML = ''; }, 4000);
  }
}