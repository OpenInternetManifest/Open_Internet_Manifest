**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters  
<button onclick="copyThesis('**Thesis 1** — Het internet is niet dood; het is gekaapt door vijf poortwachters')" class="copy-btn" title="Kopieer voor verificatie">📋</button>

**Thesis 2** — Zij die het open internet hebben ingesloten verkopen je nu het verhaal dat echte vrijheid iets uit de jaren tachtig was  
<button onclick="copyThesis('**Thesis 2** — Zij die het open internet hebben ingesloten verkopen je nu het verhaal dat echte vrijheid iets uit de jaren tachtig was')" class="copy-btn" title="Kopieer voor verificatie">📋</button>

<script>
function copyThesis(text) {
  navigator.clipboard.writeText(text).then(() => {
    // Optioneel: een subtiele feedback (geen irritante alert)
    const feedback = document.createElement('span');
    feedback.textContent = ' ✅ Gekopieerd!';
    feedback.style.color = 'green';
    feedback.style.fontSize = '0.8em';
    feedback.style.marginLeft = '5px';
    // Voeg tijdelijk toe naast de button (simpel, geen ID nodig)
    event.target.parentNode.appendChild(feedback);
    setTimeout(() => feedback.remove(), 2000);
  }).catch(() => {
    alert('Kopiëren mislukt – probeer handmatig te selecteren.');
  });
}
</script>

<style>
.copy-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1em;
  margin-left: 10px;
  opacity: 0.7;
}
.copy-btn:hover {
  opacity: 1;
}
</style>
