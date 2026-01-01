// Maak functies globaal beschikbaar voor onclick
window.copyPageText = function() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) return;

  const clone = mainContent.cloneNode(true);

  // Verwijder alle ongewenste elementen
  const toRemove = clone.querySelectorAll(`
    .copy-container,
    .integrity-check,
    .community-box,
    .donation-section,
    .site-footer,
    .footer-nav,
    .site-footer-credits,
    .page-footer,
    .copy-feedback,
    #verify-feedback,
    .verify-section,
    .hash-verifier,
    .custom-header,
    .banner,
    .overlay-text,
    .home-container,
    .language-buttons,
    .home-note,
    .manifest-header,
    .manifest-subtitle,
    .intro-title,
    .intro-text,
    .theses-list,
    .guides-list,
    .language-selector,
    h2,
    h3
  `);
  toRemove.forEach(el => el.remove());

  // Verwijder alle links (navigation)
  clone.querySelectorAll('a').forEach(a => a.remove());

  let text = clone.textContent || clone.innerText || '';
  text = text.trim().replace(/\n{3,}/g, '\n\n');

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