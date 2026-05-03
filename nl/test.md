---
layout: default
lang: nl
title: "Nexus Quick Post"
slug: nexus-quick-post
---

<div class="nexus-quick-post-container">
  <header class="quick-post-header">
    <h1>Nexus Quick Post</h1>
    <p class="subtitle">Maak een mooie post met Unicode-opmaak + automatische hash-verificatie</p>
    <div class="powered-by">Powered by OIM × Nexus</div>
  </header>

  <div class="editor-split">
    <div class="editor-panel">
      <div class="toolbar">
        <button onclick="formatBold()">𝐁</button>
        <button onclick="formatItalic()">𝐼</button>
        <button onclick="formatList()">• Lijst</button>
        <button onclick="insertQuote()">„ Citaat</button>
        <button onclick="insertEmoji()">😊</button>
      </div>
      
      <textarea id="post-input" placeholder="Typ of plak je tekst hier..."></textarea>
    </div>

    <div class="preview-panel">
      <h3>Facebook Preview</h3>
      <div id="fb-preview" class="facebook-preview-box"></div>
    </div>
  </div>

  <div class="actions-bar">
    <button onclick="generateHashAndSignature()" class="btn-primary">🔐 Generate Hash + Signature</button>
    <button onclick="copyForFacebook()" class="btn-secondary">📋 Copy for Facebook</button>
  </div>

  <div id="result" class="result-area"></div>
</div>

<style>
  .nexus-quick-post-container {
    max-width: 1200px;
    margin: 2em auto;
    padding: 2.5em;
    background: #f8fafc;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }

  .quick-post-header h1 {
    font-size: 2.4em;
    background: linear-gradient(90deg, #1e40af, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .facebook-preview-box {
    padding: 1.5em;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    min-height: 420px;
    color: #1e40af;
    font-size: 1.05em;
    line-height: 1.65;
    white-space: pre-wrap;
  }

  .actions-bar {
    display: flex;
    gap: 1.2em;
    justify-content: center;
    margin: 2.5em 0;
  }

  .btn-primary {
    background: linear-gradient(90deg, #1e40af, #22d3ee);
    color: white;
    padding: 1.1em 2.2em;
    border: none;
    border-radius: 12px;
  }

  .btn-secondary {
    background: #f1f5f9;
    color: #334155;
    padding: 1.1em 2.2em;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
  }
</style>

<script>
  const input = document.getElementById('post-input');
  const preview = document.getElementById('fb-preview');

  function updatePreview() {
    let text = input.value || "Je post verschijnt hier...";

    // Alleen vet en cursief
    text = text.replace(/\*\*(.+?)\*\*/g, (match, p1) => p1.split('').map(c => {
      const m = {'a':'𝐚','b':'𝐛','c':'𝐜','d':'𝐝','e':'𝐞','f':'𝐟','g':'𝐠','h':'𝐡','i':'𝐢',
                 'j':'𝐣','k':'𝐤','l':'𝐥','m':'𝐦','n':'𝐧','o':'𝐨','p':'𝐩','q':'𝐪','r':'𝐫',
                 's':'𝐬','t':'𝐭','u':'𝐮','v':'𝐯','w':'𝐰','x':'𝐱','y':'𝐲','z':'𝐳',
                 'A':'𝐀','B':'𝐁','C':'𝐂','D':'𝐃','E':'𝐄','F':'𝐅','G':'𝐆','H':'𝐇','I':'𝐈',
                 'J':'𝐉','K':'𝐊','L':'𝐋','M':'𝐌','N':'𝐍','O':'𝐎','P':'𝐏','Q':'𝐐','R':'𝐑',
                 'S':'𝐒','T':'𝐓','U':'𝐔','V':'𝐕','W':'𝐖','X':'𝐗','Y':'𝐘','Z':'𝐙'};
      return m[c] || c;
    }).join(''));

    text = text.replace(/\*(.+?)\*/g, (match, p1) => p1.split('').map(c => {
      const m = {'a':'𝘢','b':'𝘣','c':'𝘤','d':'𝘥','e':'𝘦','f':'𝘧','g':'𝘨','h':'𝘩','i':'𝘪',
                 'j':'𝘫','k':'𝘬','l':'𝘭','m':'𝘮','n':'𝘯','o':'𝘰','p':'𝘱','q':'𝘲','r':'𝘳',
                 's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻'};
      return m[c] || c;
    }).join(''));

    preview.textContent = text;
  }

  input.addEventListener('input', updatePreview);

  function copyForFacebook() {
    let text = input.value.trim();
    if (!text) return;

    text = text.replace(/\*\*(.+?)\*\*/g, (match, p1) => p1.split('').map(c => {
      const m = {'a':'𝐚','b':'𝐛','c':'𝐜','d':'𝐝','e':'𝐞','f':'𝐟','g':'𝐠','h':'𝐡','i':'𝐢',
                 'j':'𝐣','k':'𝐤','l':'𝐥','m':'𝐦','n':'𝐧','o':'𝐨','p':'𝐩','q':'𝐪','r':'𝐫',
                 's':'𝐬','t':'𝐭','u':'𝐮','v':'𝐯','w':'𝐰','x':'𝐱','y':'𝐲','z':'𝐳',
                 'A':'𝐀','B':'𝐁','C':'𝐂','D':'𝐃','E':'𝐄','F':'𝐅','G':'𝐆','H':'𝐇','I':'𝐈',
                 'J':'𝐉','K':'𝐊','L':'𝐋','M':'𝐌','N':'𝐍','O':'𝐎','P':'𝐏','Q':'𝐐','R':'𝐑',
                 'S':'𝐒','T':'𝐓','U':'𝐔','V':'𝐕','W':'𝐖','X':'𝐗','Y':'𝐘','Z':'𝐙'};
      return m[c] || c;
    }).join(''));

    text = text.replace(/\*(.+?)\*/g, (match, p1) => p1.split('').map(c => {
      const m = {'a':'𝘢','b':'𝘣','c':'𝘤','d':'𝘥','e':'𝘦','f':'𝘧','g':'𝘨','h':'𝘩','i':'𝘪',
                 'j':'𝘫','k':'𝘬','l':'𝘭','m':'𝘮','n':'𝘯','o':'𝘰','p':'𝘱','q':'𝘲','r':'𝘳',
                 's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻'};
      return m[c] || c;
    }).join(''));

    navigator.clipboard.writeText(text).then(() => {
      alert("✅ Gekopieerd voor Facebook!");
      window.open('https://www.facebook.com/sharer/sharer.php', '_blank');
    });
  }

  updatePreview();
</script>