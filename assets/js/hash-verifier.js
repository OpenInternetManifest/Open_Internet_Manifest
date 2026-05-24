document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  // ==================== FUZZY CLEAN ====================
  function fuzzyClean(text) {
    if (!text || typeof text !== 'string') return '';

    let t = text.replace(/^---\s*\n[\s\S]*?\n---\s*\n/s, '');
    t = t.normalize('NFKC');

    // Opmaak strippen
    t = t.replace(/\*\*(.*?)\*\*/gs, '$1');
    t = t.replace(/__(.*?)__/gs, '$1');
    t = t.replace(/\*(.*?)\*/gs, '$1');
    t = t.replace(/_(.*?)_/gs, '$1');
    t = t.replace(/^#{1,6}\s+/gm, '');
    t = t.replace(/^>\s*/gm, '');
    t = t.replace(/^\s*[-*+]\s+/gm, ' ');
    t = t.replace(/^\s*\d+\.\s+/gm, ' ');
    t = t.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
    t = t.replace(/!\[.*?\]\(.*?\)/g, '');
    t = t.replace(/`([^`]+)`/g, '$1');
    t = t.replace(/^-{3,}\s*$/gm, '');
    t = t.replace(/<[^>]+>/g, '');

    t = t.replace(/\s+/g, ' ').trim().toLowerCase();
    return t;
  }

  async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

    // Robuuste en eenvoudige similarity check
  function calculateSimilarity(text1, text2) {
    const clean1 = fuzzyClean(text1);
    const clean2 = fuzzyClean(text2);
    
    if (clean1.length === 0 || clean2.length === 0) return 0;

    // Woord-gebaseerde Jaccard similarity (zeer robuust)
    const words1 = new Set(clean1.split(/\s+/).filter(w => w.length > 2));
    const words2 = new Set(clean2.split(/\s+/).filter(w => w.length > 2));

    const intersection = [...words1].filter(word => words2.has(word)).length;
    const union = words1.size + words2.size - intersection;

    let score = union > 0 ? Math.round((intersection / union) * 100) : 0;

    // Karakter overlap als backup
    const len1 = clean1.length;
    const len2 = clean2.length;
    const minLen = Math.min(len1, len2);
    let charMatches = 0;
    for (let i = 0; i < minLen; i++) {
      if (clean1[i] === clean2[i]) charMatches++;
    }
    const charScore = Math.round((charMatches / Math.max(len1, len2)) * 100);

    // Combineer (meer gewicht op woorden)
    score = Math.round(score * 0.75 + charScore * 0.25);

    // Mildere straf voor lengteverschil
    const lengthDiff = Math.abs(len1 - len2);
    if (lengthDiff > 0) {
      score = Math.max(55, score - Math.floor(lengthDiff * 0.12));
    }

    if (lengthDiff > 0 && score >= 100) score = 99;

    return Math.min(100, score);
  }

  

  // ==================== MAIN VERIFIER ====================
  btn.addEventListener('click', async () => {
    result.style.display = 'none';
    const rawText = input.value.trim();

    if (!rawText) {
      result.innerHTML = '<span style="color:#ffaa66;">Plak eerst een tekst om te verifiëren.</span>';
      result.style.display = 'block';
      return;
    }

    const cleanText = fuzzyClean(rawText);
    const computedHash = await sha256(cleanText);

    let html = '';

    // Exacte match
    if (window.officialFuzzyHashes && window.officialFuzzyHashes[computedHash]) {
      const url = window.officialFuzzyHashes[computedHash];
      html = `
        <span style="color:#66ff66; font-size:1.9em;">✅ 100% AUTHENTIEK!</span><br><br>
        <strong>Post:</strong> <a href="https://openinternetmanifest.org/${url.replace('.md','')}" target="_blank" style="color:#66b3ff;">${url}</a>`;
    } 
    // Probability check
    else if (window.officialCleanTexts) {
      let bestMatch = null;
      let bestScore = 0;

      for (let path in window.officialCleanTexts) {
        const score = calculateSimilarity(rawText, window.officialCleanTexts[path]);
        if (score > bestScore) {
          bestScore = score;
          bestMatch = path;
        }
      }

      if (bestScore > 65) {
        html = `
          <span style="color:#ffcc66; font-size:1.6em;">⚠️ ${bestScore}% overeenstemming</span><br><br>
          <strong>Beste match:</strong> <a href="https://openinternetmanifest.org/${bestMatch.replace('.md','')}" target="_blank">${bestMatch}</a>`;
      } else {
        html = `
          <span style="color:#ff6666;">Geen goede match gevonden</span><br><br>
          <strong>Berekende hash:</strong><br>
          <code style="word-break:break-all;">${computedHash}</code>`;
      }
    }

    result.innerHTML = html;
    result.style.display = 'block';
  });
});