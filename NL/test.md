# Test voor kopieer-button

**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters  
<button onclick="copyThesis('**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters')" class="copy-btn" title="Kopieer voor verificatie">📋 Kopieer</button>

**Thesis 2** — Zij die het open internet hebben ingesloten verkopen je nu het verhaal dat echte vrijheid iets uit de jaren tachtig was  
<button onclick="copyThesis('**Thesis 2** — Zij die het open internet hebben ingesloten verkopen je nu het verhaal dat echte vrijheid iets uit de jaren tachtig was')" class="copy-btn" title="Kopieer voor verificatie">📋 Kopieer</button>

<script>
function copyThesis(text) {
  navigator.clipboard.writeText(text).then(() => {
    const feedback = document.createElement('span');
    feedback.textContent = ' ✅ Gekopieerd!';
    feedback.style.color = 'green';
    feedback.style.fontSize = '0.8em';
    feedback.style.marginLeft = '5px';
    event.target.parentNode.appendChild(feedback);
    setTimeout(() => feedback.remove(), 2000);
  }).catch(() => {
    alert('Kopiëren mislukt – probeer handmatig.');
  });
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
  padding: 2px 6px;
}
.copy-btn:hover {
  background: #f0f0f0;
}
</style>
