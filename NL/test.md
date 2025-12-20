<script>
function copyThesis(text) {
  // Probeer moderne Clipboard API
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      showFeedback(' ✅ Gekopieerd!');
    }).catch(() => {
      fallbackCopy(text);
    });
  } else {
    // Fallback voor oudere browsers of restrictieve context
    fallbackCopy(text);
  }
}

function fallbackCopy(text) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand('copy');
    showFeedback(' ✅ Gekopieerd!');
  } catch (err) {
    showFeedback(' ❌ Kopiëren mislukt');
  }
  document.body.removeChild(textarea);
}

function showFeedback(message) {
  const feedback = document.createElement('span');
  feedback.textContent = message;
  feedback.style.marginLeft = '10px';
  feedback.style.fontSize = '0.9em';
  if (message.includes('✅')) feedback.style.color = 'green';
  if (message.includes('❌')) feedback.style.color = 'red';
  event.target.parentNode.appendChild(feedback);
  setTimeout(() => feedback.remove(), 3000);
}
</script>
