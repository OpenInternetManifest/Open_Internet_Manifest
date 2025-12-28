function copyPageText() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) {
    console.log('Main content not found');
    return;
  }

  const clone = mainContent.cloneNode(true);

  // Verwijder alles wat geen thesis text is
  const toRemove = clone.querySelectorAll('.integrity-check, .page-footer, .community-box, .thesis-sidebar, .copy-container, .copy-feedback');
  toRemove.forEach(el => el.remove());

  let text = clone.textContent || clone.innerText || '';
  text = text.trim().replace(/\n{3,}/g, '\n\n');

  navigator.clipboard.writeText(text).then(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) {
      feedback.textContent = '✓ Volledige thesis tekst gekopieerd!';
      setTimeout(() => feedback.textContent = '', 3000);
    }
  }).catch(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) feedback.textContent = 'Copy mislukt – selecteer handmatig';
  });
}