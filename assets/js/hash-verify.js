function copyPageText() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) return;

  const clone = mainContent.cloneNode(true);

  // Verwijder de integrity-check + community box (page-footer)
  const toRemove = clone.querySelectorAll('.integrity-check, div[style*="text-align: center; margin-top: 3em"]');
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