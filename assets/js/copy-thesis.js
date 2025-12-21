function copyThesis(text) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      showFeedback('✅ Gekopieerd! Plak in sha256.online om te verifiëren');
    }).catch(() => {
      fallbackCopy(text);
    });
  } else {
    fallbackCopy(text);
  }
}

function fallbackCopy(text) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  try {
    document.execCommand('copy');
    showFeedback('✅ Gekopieerd! Plak in sha256.online om te verifiëren');
  } catch (err) {
    showFeedback('❌ Mislukt – probeer handmatig');
  }
  document.body.removeChild(textarea);
}

function showFeedback(message) {
  // Simpele alert voor nu; pas aan als nodig voor per-button feedback
  alert(message);
}

// Bind buttons (run na load als nodig)
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault(); // Als nodig
  });
});
