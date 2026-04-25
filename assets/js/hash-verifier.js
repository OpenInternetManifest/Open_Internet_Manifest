document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  if (typeof window.officialFuzzyHashes === 'undefined') {
    result.innerHTML = '<span style="color: #ff6666;">Error: Hashes niet geladen. Vernieuw de pagina.</span>';
    result.style.display = 'block';
    return;
  }

  // ==================== DEBUG INSTELLING ====================
  const DEBUG = true;        // Zet dit op false als je de console schoon wilt

  btn.addEventListener('click', () => {
    const rawText = input.value.trim();
    if (!rawText) {
      showResult('Plak eerst een tekst om te verifiëren.', 'warning');
      return;
    }

    // === EXACTE fuzzy cleaning (zelfde als Python + bash) ===
    let cleanText = rawText
      .replace(/\*\*\(.*?\)\*\*/g, '$1')
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/\*(.*?)\*/g, '$1')
      .replace(/^>[ \t]*/gm, '')
      .replace(/^[ \t]*###*[ \t]*/gm, '')
      .replace(/^[ \t]*[0-9]+\.[ \t]*/gm, '')
      .replace(/^[ \t]*[-*+][ \t]*/gm, '')
      .replace(/^[ \t]+/gm, '')
      .replace(/[ \t]+$/gm, '')
      .replace(/\| ?/g, ' ')
      .replace(/ \|/g, ' ')
      .replace(/^[-:| ]+$/gm, '')
      .replace(/^--$/gm, '')
      .replace(/^---$/gm, '')
      
      // Emoji normalisatie
      .replace(/😎/g, '8)')
      .replace(/😊/g, ':)')
      .replace(/😂/g, 'haha')
      .replace(/❤️/g, 'hart')
      .replace(/👍/g, 'duim')
      .replace(/👎/g, 'duim omlaag')
      .replace(/🚀/g, 'rocket')
      .replace(/🔥/g, 'vuur')
      
      .toLowerCase()
      .replace(/[ \t]+/g, ' ')
      .replace(/\n/g, ' ')
      .replace(/[ \t]+/g, ' ')
      .trim();

    // ==================== DEBUG OUTPUT ====================
    if (DEBUG) {
      console.log("%c=== HASH VERIFIER DEBUG ===", "color:#66ff66; font-weight:bold");
      console.log("Raw length:", rawText.length);
      console.log("Cleaned fuzzy text:", cleanText);
      console.log("Cleaned length:", cleanText.length);
    }

    sha256(cleanText).then(hash => {
      if (DEBUG) {
        console.log("Calculated hash:", hash);
      }

      let matchFound = false;

      for (let url in window.officialFuzzyHashes) {
        if (window.officialFuzzyHashes[url] === hash) {
          matchFound = true;
          const info = window.officialGitInfo[url] || {};
          const title = info.title || 'Onbekende post';

          let html = `<span style="color: #66ff66; font-size: 1.3em;">✅ 100% AUTHENTIEK!</span><br><br>`;
          html += `<strong>Post:</strong> <a href="${url}" target="_blank">${title}</a><br>`;
          if (info.commit_hash) {
            html += `<strong>Commit:</strong> <a href="${info.commit_url}" target="_blank">${info.commit_hash.substring(0,12)}</a> (${info.commit_date})`;
          }
          showResult(html, 'success');
          return;
        }
      }

      showResult(`❌ Geen match gevonden.<br><br>Je berekende hash:<br><code>${hash}</code>`, 'error');
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