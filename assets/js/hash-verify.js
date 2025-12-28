function copyPageText(button) {
  // Vind de bovenliggende <li>
  const li = button.closest('li');
  if (!li) return;

  // Clone de li
  const clone = li.cloneNode(true);

  // Verwijder de copy knop zelf
  const copyBtn = clone.querySelector('.copy-btn');
  if (copyBtn) copyBtn.remove();

  let text = clone.textContent || clone.innerText || '';
  text = text.trim().replace(/\n{3,}/g, '\n\n');

  navigator.clipboard.writeText(text).then(() => {
    // Feedback naast de knop
    const feedback = document.createElement('span');
    feedback.textContent = ' ✓ Gekopieerd!';
    feedback.style.color = '#66b3ff';
    feedback.style.marginLeft = '1em';
    feedback.style.fontWeight = 'bold';
    button.parentNode.appendChild(feedback);
    setTimeout(() => feedback.remove(), 3000);
  }).catch(() => {
    alert('Copy mislukt – selecteer handmatig');
  });
}