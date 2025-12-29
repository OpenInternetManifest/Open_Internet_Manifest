function copyPageText() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) return;

  const clone = mainContent.cloneNode(true);

  // Verwijder alle includes + feedback + donation section
  const toRemove = clone.querySelectorAll(
    '.integrity-check, .community-box, .donation-section, .page-footer, .copy-container, #copy-feedback, #verify-feedback'
  );
  toRemove.forEach(el => el.remove());

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
}

function verifyHash() {
  const userHash = document.getElementById('user-hash').value.trim().toLowerCase();
  if (!userHash) {
    const lang = document.documentElement.lang || 'nl';
    const noHashText = lang === 'en' ? '✗ Enter a hash' : '✗ Voer een hash in';
    document.getElementById('verify-feedback').innerHTML = `<span style="color: #ff6666 !important;">${noHashText}</span>`;
    return;
  }

  let pagePath = window.location.pathname;
  pagePath = pagePath.replace(/\/$/, '').replace(/^\/Open_Internet_Manifest/, '');

  const expectedHash = getExpectedHash(pagePath);

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
}

// Map van page paths naar hashes (zonder baseurl en trailing slash)
function getExpectedHash(path) {
  const hashes = {
    '/NL/theses/thesis-01': '4aa8a37884deb164c85153f32f9b300f3e210fe207ff1bbcd896f0706ab7f9cd',
    '/NL/theses/thesis-02': 'ffa4081242a6fdc994dfe0086e54fb0c6aaebc1b266a42626ce9ceeb040317d4',
    '/NL/theses/thesis-03': '2b8ef75f77107c57c3f916c358a0a6d4126dc47890ca74c1e89c5ab05b84a37f',
    '/NL/manifest': 'voorbeeldhashvoormanifest',
    // Voeg de rest toe als je ze hebt
  };
  return hashes[path] || null;
}