function copyPageText() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) return;

  const clone = mainContent.cloneNode(true);

  // Verwijder integrity-check + community box + footer + copy knoppen
  const toRemove = clone.querySelectorAll('.integrity-check, .community-box, .page-footer, .copy-container');
  toRemove.forEach(el => el.remove());

  let text = clone.textContent || clone.innerText || '';
  text = text.trim().replace(/\n{3,}/g, '\n\n');

  navigator.clipboard.writeText(text).then(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) {
      feedback.textContent = '✓ Pagina tekst gekopieerd!';
      setTimeout(() => feedback.textContent = '', 3000);
    }
  }).catch(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) feedback.textContent = 'Copy mislukt – selecteer handmatig';
  });
}

function verifyHash() {
  const userHash = document.getElementById('user-hash').value.trim().toLowerCase();
  if (!userHash) {
    document.getElementById('verify-feedback').innerHTML = '<span style="color: #ff6666;">✗ Voer een hash in</span>';
    return;
  }

  let pagePath = window.location.pathname;
  pagePath = pagePath.replace(/\/$/, '').replace(/^\/Open_Internet_Manifest/, '');

  const expectedHash = getExpectedHash(pagePath);

  const feedback = document.getElementById('verify-feedback');

  if (userHash === expectedHash) {
   feedback.textContent = '✓ Pagina tekst gekopieerd!';
    feedback.innerHTML = `<span style="color: #ff6666;">✗ Geen match</span><br>
      Jouw hash: <code style="word-break: break-all;">${userHash}</code><br>
      Officiële hash: <code style="word-break: break-all;">${expectedHash || 'niet gevonden'}</code>`;
  }
}

// Map van page paths naar hashes (zonder baseurl en trailing slash)
function getExpectedHash(path) {
  const hashes = {
    '/NL/theses/thesis-01': '4aa8a37884deb164c85153f32f9b300f3e210fe207ff1bbcd896f0706ab7f9cd',
    '/NL/theses/thesis-02': 'ffa4081242a6fdc994dfe0086e54fb0c6aaebc1b266a42626ce9ceeb040317d4',
    '/NL/theses/thesis-03': '2b8ef75f77107c57c3f916c358a0a6d4126dc47890ca74c1e89c5ab05b84a37f',
    // Voeg de rest toe als je ze hebt
    '/NL/manifest': 'voorbeeldhashvoormanifest',
  };
  return hashes[path] || null;
}