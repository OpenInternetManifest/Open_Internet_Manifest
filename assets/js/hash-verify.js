function copyThesisText() {
  // Haal de main content text op (exclusief details, footer, etc.)
  const mainContent = document.querySelector('.main-content');
  let text = '';
  if (mainContent) {
    // Clone om hidden elements te vermijden
    const clone = mainContent.cloneNode(true);
    // Verwijder de integrity-check en footer
    const details = clone.querySelector('.integrity-check');
    if (details) details.remove();
    const footer = clone.querySelector('.site-footer');
    if (footer) footer.remove();
    text = clone.textContent.trim();
  }

  navigator.clipboard.writeText(text).then(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) {
      feedback.textContent = '✓ Thesis tekst gekopieerd!';
      setTimeout(() => feedback.textContent = '', 3000);
    }
  }).catch(err => {
    console.error('Copy failed', err);
    const feedback = document.getElementById('copy-feedback');
    if (feedback) feedback.textContent = 'Copy mislukt – selecteer handmatig';
  });
}