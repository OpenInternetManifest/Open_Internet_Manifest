# Test voor kopieer-button

**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters  
<button onclick="copyThesis('**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters')" class="copy-btn" title="Kopieer voor verificatie">📋 Kopieer</button>

**Thesis 2** — Zij die het open internet hebben ingesloten verkopen je nu het verhaal dat echte vrijheid iets uit de jaren tachtig was  
<button onclick="copyThesis('**Thesis 2** — Zij die het open internet hebben ingesloten verkopen je nu het verhaal dat echte vrijheid iets uit de jaren tachtig was')" class="copy-btn" title="Kopieer voor verificatie">📋 Kopieer</button>

<script>
function copyThesis(text) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      showFeedback(' ✅ Gekopieerd!');
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

<style>
.copy-btn {
  background: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8em;
  margin-left: 10px;
  padding: 4px 8px;
}
.copy-btn:hover {
  background: #f0f0f0;
}
</style>
