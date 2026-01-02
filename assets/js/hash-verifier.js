document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  if (typeof officialHashes === 'undefined') {
    showResult('Error: hashes niet geladen. Vernieuw de pagina.', 'error');
    return;
  }

  const hasPreStored = typeof preStoredTexts !== 'undefined' && Object.keys(preStoredTexts).length > 0;

  btn.addEventListener('click', () => {
    const rawText = input.value.trim();
    if (!rawText) {
      showResult('Voer een tekst in.', 'warning');
      return;
    }

    let cleanText = rawText
      .replace(/\r\n/g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .replace(/[ \t]+/g, ' ')
      .trim();

    sha256(cleanText).then(computedHash => {
      computedHash = computedHash.toLowerCase();

      // 1. Exacte hash-match → groen
      const exactMatch = Object.entries(officialHashes).find(([path, h]) => h.toLowerCase() === computedHash);
      if (exactMatch) {
        const [path] = exactMatch;
        const url = `https://openinternetmanifest.github.io/Open_Internet_Manifest${path}`;
        showResult(`✅ <strong>100% authentiek!</strong><br>Deze tekst komt exact overeen met:<br><a href="${url}" target="_blank">${getTitle(path)}</a>`, 'success');
        return;
      }

           // 2. Fuzzy match op tekst – altijd geel als gevonden
      if (hasPreStored) {
        let bestMatch = null;
        let bestRatio = 0;

        for (const [path, storedText] of Object.entries(preStoredTexts)) {
          const ratio = stringSimilarity(cleanText, storedText);
          if (ratio > bestRatio) {
            bestRatio = ratio;
            bestMatch = path;
          }
        }

        if (bestMatch && bestRatio >= 0.85) {
          const url = `https://openinternetmanifest.github.io/Open_Internet_Manifest${bestMatch}`;
          showResult(`⚠️ Geen exacte hash-match, maar zeer goed overeenkomt met:<br><a href="${url}" target="_blank">${getTitle(bestMatch)}</a><br><small>Dit is waarschijnlijk de juiste thesis – mogelijk kleine kopieerfout (puntje, spatie of enter).</small>`, 'warning');
          return;
        }
      }
      // 3. Geen match
      showResult('❌ Geen match gevonden – dit lijkt geen tekst uit het Open Internet Manifest.', 'error');
    }).catch(() => {
      showResult('Fout bij berekenen hash. Probeer opnieuw.', 'error');
    });
  });

  function showResult(message, type) {
    result.innerHTML = message;
    result.className = `result-box ${type}`;
    result.style.display = 'block';
  }

  function getTitle(path) {
    if (path === '' || path === '/nl' || path === '/nl/') return 'Manifest overzicht (NL)';
    if (path === '/en' || path === '/en/') return 'Manifest overview (EN)';
    if (path.includes('/theses/thesis-')) {
      const num = path.split('-').pop();
      return path.includes('/nl/') ? `Thesis ${num} (NL)` : `Thesis ${num} (EN)`;
    }
    if (path.includes('/begrippen/')) return 'Begrip: ' + path.split('/').pop();
    if (path.includes('/concepts/')) return 'Concept: ' + path.split('/').pop();
    if (path.includes('/guides/')) return 'Guide: ' + path.split('/').pop();
    return path || 'Home';
  }

  async function sha256(str) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

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