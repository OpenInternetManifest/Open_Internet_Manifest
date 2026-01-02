// Maak functies globaal beschikbaar voor onclick
window.copyPageText = function() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) return;

  const clone = mainContent.cloneNode(true);

  // === VERWIJDER ALLE ONGEWENSTE ELEMENTEN ===
  const selectorsToRemove = [
    // Integrity check volledig
    '.integrity-check',
    '.integrity-content',
    '.copy-container',
    '.verify-section',
    '.hash-verifier',
    '.copy-feedback',
    '#verify-feedback',
    '.verify-feedback',

    // Andere niet-inhoud elementen
    '.community-box',
    '.donation-section',
    '.site-footer',
    '.footer-nav',
    '.site-footer-credits',
    '.page-footer',
    '.banner',
    '.overlay-text',
    '.custom-header',

    // Homepage/taalkiezer elementen
    '.home-container',
    '.language-buttons',
    '.home-note',
    '.language-selector',

    // Hoofdtitels en intro's die je niet in de pure tekst wilt
    '.manifest-header',
    '.manifest-subtitle',
    '.intro-title',
    '.intro-text',

    // Alle kopjes (h1 t/m h6) – want die wil je niet in de hash-tekst
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',

    // Alle navigatie links
    'a'
  ];

  // Verwijder al deze elementen
  clone.querySelectorAll(selectorsToRemove.join(', ')).forEach(el => el.remove());

  // Extra veiligheid: verwijder ook eventuele overgebleven lege paragrafen/divs
  clone.querySelectorAll('p, div, section').forEach(el => {
    if (el.textContent.trim() === '' || el.children.length === 0 && el.textContent.trim().length < 10) {
      el.remove();
    }
  });

  // Haal de pure tekst op
  let text = clone.textContent || clone.innerText || '';
  text = text
    .replace(/\s+/g, ' ')     // Meerdere spaties/newlines → enkele spatie
    .replace(/\n{3,}/g, '\n\n') // Max 2 newlines
    .trim();

  // Kopieer naar klembord
  navigator.clipboard.writeText(text).then(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) {
      const lang = document.documentElement.lang || 'nl';
      const copiedText = lang === 'en' ? '✓ Page text copied!' : '✓ Pagina tekst gekopieerd!';
      feedback.innerHTML = `<span style="color: #66ff66 !important; font-weight: bold;">${copiedText}</span>`;
      setTimeout(() => feedback.innerHTML = '', 3000);
    }
  }).catch(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) {
      const lang = document.documentElement.lang || 'nl';
      const errorText = lang === 'en' ? 'Copy failed – select manually' : 'Copy mislukt – selecteer handmatig';
      feedback.innerHTML = `<span style="color: #ff6666 !important;">${errorText}</span>`;
    }
  });
};

// verifyHash blijft ongewijzigd – die werkt al goed
window.verifyHash = function() {
  const userHash = document.getElementById('user-hash').value.trim().toLowerCase();
  if (!userHash) {
    const lang = document.documentElement.lang || 'nl';
    const noHashText = lang === 'en' ? '✗ Enter a hash' : '✗ Voer een hash in';
    document.getElementById('verify-feedback').innerHTML = `<span style="color: #ff6666 !important;">${noHashText}</span>`;
    return;
  }

  let pagePath = window.location.pathname;
  pagePath = pagePath.replace(/\/$/, '').replace(/^\/Open_Internet_Manifest/, '');

  const expectedHash = officialHashes[pagePath] || null;

  const feedback = document.getElementById('verify-feedback');
  const lang = document.documentElement.lang || 'nl';

  if (userHash === expectedHash) {
    const matchText = lang === 'en' ? '✓ PERFECT MATCH!' : '✓ PERFECTE MATCH!';
    const authText = lang === 'en' ? 'This page is 100% authentic.' : 'Deze pagina is 100% authentiek.';
    feedback.innerHTML = `<span style="color: #66ff66 !important; font-size: 1.2em; font-weight: bold;">${matchText}</span> ${authText}`;
  } else {
    const noMatchText = lang === 'en' ? '✗ No match' : '✗ Geen match';
    const yourHash = lang === 'en' ? 'Your hash:' : 'Jouw hash:';
    const officialHash = lang === 'en' ? 'Official hash:' : 'Officiële hash:';
    const notFound = lang === 'en' ? 'not found' : 'niet gevonden';
    feedback.innerHTML = `<span style="color: #ff6666 !important; font-weight: bold;">${noMatchText}</span><br>
      <strong>${yourHash}</strong> <code style="word-break: break-all;">${userHash}</code><br>
      <strong>${officialHash}</strong> <code style="word-break: break-all;">${expectedHash || notFound}</code>`;
  }
};