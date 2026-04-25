document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  if (typeof window.officialFuzzyHashes === 'undefined') {
    result.innerHTML = '<span style="color: #ff6666;">Error: Hashes niet geladen. Vernieuw de pagina.</span>';
    result.style.display = 'block';
    return;
  }

  btn.addEventListener('click', () => {
    const rawText = input.value.trim();
    if (!rawText) {
      showResult('Plak eerst een tekst om te verifiëren.', 'warning');
      return;
    }

    // === EXACTE fuzzy cleaning + emoji handling ===
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
      
      // Emoji cleanup - belangrijk voor social media
      .replace(/😎/g, '8)')           // sunglasses emoji → 8)
      .replace(/😊/g, ':)')           // smile
      .replace(/😂/g, 'haha')         // laugh
      .replace(/❤️/g, 'hart')         // heart
      .replace(/👍/g, 'duim')         // thumbs up
      .replace(/👎/g, 'duim omlaag')
      .replace(/🚀/g, 'rocket')
      .replace(/🔥/g, 'vuur')
      
      .toLowerCase()
      .replace(/[ \t]+/g, ' ')
      .replace(/\n/g, ' ')
      .replace(/[ \t]+/g, ' ')
      .trim();

    // === DEBUG OUTPUT ===
    console.log("=== RAW TEXT ===");
    console.log(rawText);
    console.log("\n=== CLEANED FUZZY TEXT (wat de verifier gebruikt) ===");
    console.log(cleanText);
    console.log("\n=== LENGTH ===");
    console.log("Raw:", rawText.length, "| Clean:", cleanText.length);

    sha256(cleanText).then(hash => {
      console.log("=== CALCULATED HASH ===");
      console.log(hash);

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