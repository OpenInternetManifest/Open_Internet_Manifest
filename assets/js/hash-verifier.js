document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  // Alle officiële hashes (kopieer uit je hash-verify.js – alleen de hashes, geen paths nodig voor fuzzy)
  const officialHashes = {
    // Voorbeeld – vul met jouw hashes uit hash-verify.js
    "d25d5099dca24666730cd235ce624f4a68f3ae15dcfa6246618b82f49b51fb0d": "/nl/theses/thesis-01",
    "4ee65e950c5bc52e05afc5c34255c0863da60552cdf743a6f174fac8dcbd4246": "/nl/theses/thesis-02",
    // ... alle hashes + paden
  };

  // Pre-stored clean texts voor fuzzy match (optioneel, maar aanbevolen voor snelheid)
  const preStoredTexts = {
    "/nl/theses/thesis-01": "Thesis 1\n\nHet internet is niet dood; het is gekaapt door vijf poortwachters die 92% van onze digitale adem controleren.\n\nWaar wij vroeger vrij door een open veld liepen, staan nu Apple, Google, Microsoft, Amazon en Meta als gewapende landheren aan elk kruispunt, tol heffend over elke stap, elk woord, elke gedachte.\n\nZij bepalen welke wegen zichtbaar zijn, welke stemmen doorkomen, welke apparaten nog mogen spreken met elkaar.\n\nZolang hun greep niet wordt gebroken, blijft digitale soevereiniteit een sprookje dat wij onze kinderen vertellen terwijl zij opgroeien in ommuurde tuinen.",
    // vul voor alle pages (kan met script gegenereerd worden)
  };

  btn.addEventListener('click', () => {
    const rawText = input.value.trim();
    if (!rawText) {
      showResult('Voer een tekst in.', 'warning');
      return;
    }

    // Clean text exact zoals copyPageText()
    let cleanText = rawText.trim();
    cleanText = cleanText.replace(/\n{3,}/g, '\n\n');

    // Bereken hash
    sha256(cleanText).then(hash => {
      // Exact match
      if (officialHashes[hash]) {
        const path = officialHashes[hash];
        const url = `https://openinternetmanifest.github.io${path}`;
        showResult(`✅ <strong>100% authentiek!</strong><br>Deze tekst komt exact overeen met:<br><a href="${url}" target="_blank">${getTitle(path)}</a>`, 'success');
        return;
      }

      // Fuzzy match als geen exact
      let bestMatch = null;
      let bestRatio = 0;

      for (const [path, storedText] of Object.entries(preStoredTexts)) {
        const ratio = stringSimilarity(cleanText, storedText);
        if (ratio > bestRatio && ratio >= 0.85) { // threshold 85%
          bestRatio = ratio;
          bestMatch = path;
        }
      }

      if (bestMatch) {
        const url = `https://openinternetmanifest.github.io${bestMatch}`;
        showResult(`⚠️ Geen exacte match, maar <strong>${Math.round(bestRatio * 100)}% overeenkomt</strong> met:<br><a href="${url}" target="_blank">${getTitle(bestMatch)}</a><br><small>Mogelijk kleine aanpassing, kopieerfout of opmaakverschil.</small>`, 'warning');
      } else {
        showResult('❌ Geen match gevonden – dit lijkt geen tekst uit het Open Internet Manifest.', 'error');
      }
    });
  });

  function showResult(message, type) {
    result.innerHTML = message;
    result.className = `result-box ${type}`;
    result.style.display = 'block';
  }

  function getTitle(path) {
    if (path.includes('/theses/thesis-')) {
      const num = path.split('-').pop();
      return path.includes('/nl/') ? `Thesis ${num}` : `Thesis ${num}`;
    }
    if (path.includes('/begrippen/') || path.includes('/concepts/')) {
      return 'Begrip: ' + path.split('/').pop();
    }
    if (path.includes('/guides/')) {
      return 'Guide: ' + path.split('/').pop();
    }
    return path;
  }

  // SHA256 functie
  async function sha256(str) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // Simple string similarity (Damerau-Levenshtein ratio)
  function stringSimilarity(s1, s2) {
    const longer = s1.length > s2.length ? s1 : s2;
    const shorter = s1.length > s2.length ? s2 : s1;
    if (longer.length === 0) return 1.0;
    const costs = new Array();
    for (let i = 0; i <= longer.length; i++) {
      let lastValue = i;
      for (let j = 0; j <= shorter.length; j++) {
        if (i === 0) costs[j] = j;
        else {
          if (j > 0) {
            let newValue = costs[j - 1];
            if (longer.charAt(i - 1) !== shorter.charAt(j - 1))
              newValue = Math.min(newValue, lastValue, costs[j]) + 1;
            costs[j - 1] = lastValue;
            lastValue = newValue;
          }
        }
      }
      if (i > 0) costs[shorter.length] = lastValue;
    }
    return (longer.length - costs[shorter.length]) / longer.length;
  }
});