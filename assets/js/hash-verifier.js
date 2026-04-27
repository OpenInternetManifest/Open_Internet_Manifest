document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  if (typeof window.officialFuzzyHashes === 'undefined') {
    result.innerHTML = '<span style="color: #ff6666;">Error: Hashes niet geladen. Vernieuw de pagina.</span>';
    result.style.display = 'block';
    return;
  }

  const DEBUG = true;

  // ==================== FUZZY CLEAN ====================
  function fuzzyClean(text) {
    if (!text || typeof text !== 'string') return '';

    let t = text.normalize('NFKC');

    t = t.replace(/[\uD83C-\uDBFF\uDC00-\uDFFF\u2600-\u27FF\uFE0F\u200D\u2B50\u231A\u23E9-\u23FA\u25AA\u25AB\u25FB-\u25FE\u2600-\u26FF\u2700-\u27BF\u2B05-\u2B07\u2934\u2935\u2B50\u3297\u3299\u3030\u303D\u00A9\u00AE\u2122\u2139\u2194-\u2199\u21A9\u21AA\u231A\u231B\u2328\u23CF\u23E9-\u23F3\u23F8-\u23FA\u24C2\u25AA\u25AB\u25B6\u25C0\u25FB-\u25FE\u2600-\u26FF\u2705\u270A-\u270D\u270F\u2712\u2714\u2716\u271D\u2721\u2728\u2733\u2734\u2744\u2747\u274C\u274E\u2753-\u2755\u2757\u2763\u2764\u2795-\u2797\u27A1\u27B0\u27BF\u2934\u2935\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55\u3030\u303D\u3297\u3299\u00A9\u00AE\u2122\u2139]+/g, '');

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
    t = t.replace(/^-{3,}\s*$/gm, ' ');

    t = t.replace(/<[^>]+>/g, '');

    t = t.replace(/\s*\(\s*dag\s*,\s*/gi, ' (dag ');
    t = t.replace(/\s+,\s+/g, ', ');

    const titleColons = /(narratief|realiteit|hoe werkt het|hoe zien we dit|de grote verbinding|de oim-boodschap|traumabinding|cognitive dissonance|identificatie|overheid en burgers|social media|relaties en sekten|politiek|dank dat je|lees zelf|check zelf|weiger mee te spelen|schokkends|en vooral|passiviteit)/gi;
    t = t.replace(new RegExp(`(${titleColons.source})\\s*:\\s*`, 'gi'), '$1 ');

    t = t.replace(/https?:\/\//g, '___URL___');
    t = t.replace(/:/g, ' ');
    t = t.replace(/___URL___/g, 'https://');

    t = t.replace(/\s+/g, ' ').trim().toLowerCase();
    return t;
  }

   // ==================== AANGEPASTE CURVE + STERKERE N-GRAM RETURN ====================
  function calculateSimilarity(inputText) {
    try {
      const cleanInput = fuzzyClean(inputText);
      if (cleanInput.length < 30) {
        return { score: 15, url: null, title: null };
      }

      let bestScore = 0;
      let bestUrl = null;
      let bestTitle = null;

      const inputWords = cleanInput.split(/\s+/).filter(Boolean);

      for (let rawKey in window.officialCleanTexts) {
        const officialClean = window.officialCleanTexts[rawKey];
        if (!officialClean) continue;

        let displayUrl = rawKey.replace(/^_social-posts/, '/social-posts')
                              .replace(/\.md$/, '.html');

        const officialWords = officialClean.split(/\s+/).filter(Boolean);

        // Jaccard
        const set1 = new Set(inputWords);
        const set2 = new Set(officialWords);
        const intersection = [...set1].filter(w => set2.has(w)).length;
        const union = set1.size + set2.size - intersection;
        const jaccard = union === 0 ? 0 : intersection / union;

        // N-gram (3-gram) voor betere volgorde
        const inputTrigrams = getNGrams(inputWords, 3);
        const officialTrigrams = getNGrams(officialWords, 3);
        const trigramIntersection = [...inputTrigrams].filter(t => officialTrigrams.has(t)).length;
        const trigramUnion = inputTrigrams.size + officialTrigrams.size - trigramIntersection;
        const trigramScore = trigramUnion === 0 ? 0 : trigramIntersection / trigramUnion;

        const lenRatio = Math.min(cleanInput.length, officialClean.length) / Math.max(cleanInput.length, officialClean.length);

        let score = (jaccard * 0.40 + trigramScore * 0.45 + lenRatio * 0.15) * 100;

        const lengthDiff = Math.abs(cleanInput.length - officialClean.length);

        // === AANGEPASTE CURVE ===
        if (lengthDiff < 10) score += 28;           // 1 karakter → 99%
        else if (lengthDiff < 50) score += 15;      // tot 1 zin → ~90-95%
        else if (lengthDiff < 90) score -= 28;      // 1 - 1,5 zin → ~78-85%
        else if (lengthDiff < 140) score -= 58;     // 1,5 - 2,5 zin → ~68-75%
        else if (lengthDiff < 220) score -= 105;    // 3+ zinnen → ~55-65%
        else score -= (1 - lenRatio) * 240;

        score = Math.max(10, Math.min(99, Math.round(score)));

        // Zeer sterke prioriteit voor beste match
        if (score > bestScore || (Math.abs(score - bestScore) < 20 && trigramScore > 0.55)) {
          bestScore = score;
          bestUrl = displayUrl;
          bestTitle = window.officialGitInfo[rawKey]?.title || 
                      window.officialGitInfo[displayUrl]?.title || 
                      'OIM Post';
        }
      }

      if (DEBUG) {
        console.log("%c=== SIMILARITY DEBUG ===", "color:#ffaa66; font-weight:bold");
        console.log("Input length:", cleanInput.length);
        console.log("Best score:", bestScore);
        console.log("Best URL:", bestUrl);
        console.log("Best Title:", bestTitle);
      }

      return { score: Math.min(99, bestScore), url: bestUrl, title: bestTitle };

    } catch (err) {
      console.error("Error in calculateSimilarity:", err);
      return { score: 20, url: null, title: null };
    }
  }

  function getNGrams(words, n) {
    const grams = new Set();
    for (let i = 0; i <= words.length - n; i++) {
      grams.add(words.slice(i, i + n).join(' '));
    }
    return grams;
  }
  
  function getConfidenceHTML(score, bestUrl = null, bestTitle = null) {
    let color, label, explanation;

    if (score >= 95) { color = '#66ff66'; label = 'Bijna identiek'; explanation = 'Bijna perfecte overeenkomst.'; }
    else if (score >= 85) { color = '#99ff99'; label = 'Zeer waarschijnlijk authentiek'; explanation = 'Sterke inhoudelijke match.'; }
    else if (score >= 65) { color = '#ffdd66'; label = 'Waarschijnlijk dezelfde post'; explanation = 'Mogelijk kleine wijzigingen of samenvatting.'; }
    else if (score >= 40) { color = '#ffaa66'; label = 'Gedeeltelijk gerelateerd'; explanation = 'Enkele overeenkomsten, maar niet overtuigend.'; }
    else { color = '#ff6666'; label = 'Niet herkend'; explanation = 'Komt niet overeen met bekende OIM-posts.'; }

    let html = `
      <div style="margin:20px 0 15px;">
        <strong>${label}</strong><br>
        <div style="background:#333; height:18px; border-radius:999px; overflow:hidden; margin:10px 0;">
          <div style="width:${score}%; height:100%; background:${color}; transition:width 0.8s ease-in-out;"></div>
        </div>
        <span style="font-size:1.8em; font-weight:bold; color:${color};">${score}%</span>
      </div>
      <p style="color:#ccc;">${explanation}</p>
    `;

    if (bestUrl && bestTitle && score >= 40) {
      html += `<p><strong>Meest overeenkomende post:</strong> <a href="${bestUrl}" target="_blank" style="color:#66ccff;">${bestTitle}</a></p>`;
    }

    return html;
  }

  // ==================== MAIN LOGIC ====================
  btn.addEventListener('click', () => {
    const rawText = input.value.trim();
    if (!rawText) {
      result.innerHTML = '<span style="color:#ffaa66;">Plak eerst een tekst om te verifiëren.</span>';
      result.style.display = 'block';
      return;
    }

    const cleanText = fuzzyClean(rawText);

    if (DEBUG) {
      console.log("%c=== HASH VERIFIER DEBUG ===", "color:#66ff66; font-weight:bold");
      console.log("Raw length:", rawText.length);
      console.log("Cleaned length:", cleanText.length);
    }

    sha256(cleanText).then(hash => {
      // Laag 1: Exacte match
      for (let url in window.officialFuzzyHashes) {
        if (window.officialFuzzyHashes[url] === hash) {
          const info = window.officialGitInfo[url] || {};
          let html = `<span style="color:#66ff66; font-size:1.6em;">✅ 100% AUTHENTIEK!</span><br><br>`;
          html += `<strong>Post:</strong> <a href="${url}" target="_blank">${info.title || 'OIM Post'}</a>`;
          result.innerHTML = html;
          result.style.display = 'block';
          return;
        }
      }

      // Laag 2: Similarity met echte clean texts
      const sim = calculateSimilarity(rawText);
      result.innerHTML = getConfidenceHTML(sim.score, sim.url, sim.title);
      result.style.display = 'block';
    });
  });

  async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }
});