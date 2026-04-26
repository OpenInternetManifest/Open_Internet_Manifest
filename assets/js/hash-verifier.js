document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input-text');
  const btn = document.getElementById('verify-btn');
  const result = document.getElementById('result');

  if (!btn) {
    console.error("Button #verify-btn niet gevonden!");
    return;
  }

  const DEBUG = true;

  btn.addEventListener('click', () => {
    console.log("✅ Button clicked!");   // Dit moet in de console verschijnen

    const rawText = input.value.trim();
    if (!rawText) {
      showResult('Plak eerst een tekst om te verifiëren.', 'warning');
      return;
    }

    // Simpele maar robuuste cleaning
    let cleanText = rawText
      .replace(/\*\*(.+?)\*\*/g, '$1')
      .replace(/\*(.+?)\*/g, '$1')
      .replace(/__(.+?)__/g, '$1')
      .replace(/_(.+?)_/g, '$1')
      // Unicode bold/italic (meest voorkomende)
      .replace(/[\u1D400-\u1D7FF]/g, m => {
        const code = m.charCodeAt(0);
        if (code >= 0x1D400 && code <= 0x1D433) return String.fromCharCode(code - 0x1D400 + 65);
        if (code >= 0x1D434 && code <= 0x1D467) return String.fromCharCode(code - 0x1D434 + 97);
        return m;
      })
      .replace(/<[^>]+>/g, '')
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();

    if (DEBUG) {
      console.log("Raw length:", rawText.length);
      console.log("Cleaned:", cleanText.substring(0, 200) + "...");
    }

    sha256(cleanText).then(hash => {
      console.log("Hash:", hash);
      // Hier komt je matching-logica (tijdelijk uitgeschakeld voor test)
      showResult(`<span style="color:#66ff66;">Hash berekend: ${hash}</span><br><br>Test modus - matching uitgeschakeld`, 'success');
    });
  });

  function showResult(html, type) {
    result.innerHTML = html;
    result.style.display = 'block';
  }

  async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }
});