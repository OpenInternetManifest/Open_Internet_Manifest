document.addEventListener('DOMContentLoaded', () => {
  console.log("🔥 Hash Verifier v2 loaded");

  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  if (!input || !btn || !result) {
    console.error("Elements missing");
    return;
  }

  btn.addEventListener('click', () => {
    console.log("Button clicked");

    let rawText = input.value.trim();
    if (!rawText) {
      showResult('Plak eerst een tekst.', 'warning');
      return;
    }

    // FUZZY CLEANING - Probeert Python zo dicht mogelijk te benaderen
    let cleanText = rawText
      // Unicode fancy letters → normaal
      .replace(/[\uD835\uDC00-\uD835\uDFFF]/gu, (m) => {
        const code = m.codePointAt(0);
        if (code >= 0x1D400 && code <= 0x1D433) return String.fromCharCode(code - 0x1D400 + 65);
        if (code >= 0x1D434 && code <= 0x1D467) return String.fromCharCode(code - 0x1D434 + 97);
        return m;
      })
      .replace(/[𝐀-𝐙]/g, m => String.fromCharCode(m.charCodeAt(0) - 0x1D400 + 65))
      .replace(/[𝐚-𝐳]/g, m => String.fromCharCode(m.charCodeAt(0) - 0x1D41A + 97))

      // Markdown
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/\*(.*?)\*/g, '$1')
      .replace(/~~(.*?)~~/g, '$1')
      .replace(/`(.*?)`/g, '$1')
      .replace(/^>\s*/gm, '')
      .replace(/^#{1,6}\s*/gm, '')
      .replace(/^\s*[-*+]\s+/gm, '')
      .replace(/^\s*\d+\.\s+/gm, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/!\[[^\]]*\]\([^)]+\)/g, '')

      // Finale cleanup - GEEN emoji vervanging
      .toLowerCase()
      .replace(/[ \t]+/g, ' ')
      .replace(/\n+/g, ' ')
      .replace(/[ \t]+/g, ' ')
      .trim();

    console.log("=== RAW ===\n", rawText);
    console.log("=== CLEANED ===\n", cleanText);

    sha256(cleanText).then(hash => {
      console.log("=== HASH ===\n", hash);

      // Match check
      let matchFound = false;
      for (let url in window.officialFuzzyHashes) {
        if (window.officialFuzzyHashes[url] === hash) {
          matchFound = true;
          const info = window.officialGitInfo[url] || {};
          showResult(`✅ 100% AUTHENTIEK!<br><strong>${info.title || 'Post'}</strong>`, 'success');
          return;
        }
      }

      showResult(`❌ Geen match<br>Hash: <code>${hash}</code>`, 'error');
    });
  });

  function showResult(html, type) {
    result.innerHTML = html;
    result.style.display = 'block';
    result.style.borderLeftColor = type === 'success' ? '#66ff66' : '#ff6666';
  }

  async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }
});