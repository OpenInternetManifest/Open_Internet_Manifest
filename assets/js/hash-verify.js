function copyPageText() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) return;

  const clone = mainContent.cloneNode(true);

  // Verwijder de includes (integrity check + community)
  const toRemove = clone.querySelectorAll('.integrity-check, .page-footer, .community-box, .thesis-sidebar'); // Voeg classes toe als nodig
  toRemove.forEach(el => el.remove());

  // Verwijder footer als die in main zit
  const footer = clone.querySelector('.site-footer');
  if (footer) footer.remove();

  let text = clone.textContent || clone.innerText || '';
  text = text.trim().replace(/\n{3,}/g, '\n\n'); // Clean newlines

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