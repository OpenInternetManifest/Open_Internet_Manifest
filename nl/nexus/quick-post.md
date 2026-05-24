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
    <div class="powered-by">Powered by OIM ╳ Nexus</div>
  </header>

  <div class="editor-split">
    <div class="editor-panel">
      <div class="panel-header">Editor – Markdown invoer</div>
      <div class="toolbar">
        <button onclick="formatH3()" title="H3">H3</button>
        <button onclick="formatH4()" title="H4">H4</button>
        <button onclick="formatBold()" title="Bold">𝐁</button>
        <button onclick="formatItalic()" title="Italic">𝐼</button>
        <button onclick="showListMenu()" title="Lijst">• Lijst</button>
        <button onclick="insertQuote()" title="Citaat">„ Citaat</button>
        <button onclick="insertLink()" title="Link">[Link]</button>
        <button onclick="insertCode()" title="Code">`Code`</button>
        <button onclick="showEmojiMenu()" title="Emoji">😊</button>
      </div>
      
      <textarea id="post-input" placeholder="Typ of plak je tekst hier..."></textarea>
    </div>

    <div class="preview-panel">
      <div class="panel-header">Facebook Preview</div>
      <div class="preview-toolbar">
        Live voorbeeld hoe de Unicode opmaak eruit komt te zien
      </div>
      <div id="fb-preview" class="facebook-preview-box"></div>
    </div>
  </div>

  <!-- HASH + SIGNATURE BOX -->
  <div id="hash-signature" class="hash-box">
    <label class="hash-toggle">
      <input type="checkbox" id="include-hash" checked>
      <span>Include Hash + Signature</span>
    </label>

    <div class="hash-content">
      <strong>🔐 SHA256 Hash</strong><br>
      <code id="hash-value" class="hash-value">Berekenen...</code>

      <div class="copy-buttons">
        <button onclick="copyForFacebook()" class="btn-facebook">📘 Facebook</button>
        <button onclick="copyUnicodeWithSignature()" class="btn-unicode">🔠 Unicode + Signature</button>
        <button onclick="copyForX()" class="btn-x">𝕏 X/Twitter</button>
        <button onclick="copyUnicodeNoSignature()" class="btn-unicode-no-sig">🔠 Unicode (geen signature)</button>
      </div>

      <button id="submit-verification-btn" onclick="submitForVerification()" class="btn-submit" style="display:none; margin-top:16px;">
        📤 Submit post voor officiële verificatie
      </button>
    </div>
  </div>
</div>

{% include unicode-converter.html %}

<script>
  const input = document.getElementById('post-input');
  const preview = document.getElementById('fb-preview');

  // ==================== HELPER ====================
  window.insertAtCursor = function(before, after = '') {
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const selected = input.value.substring(start, end);
    input.value = input.value.substring(0, start) + before + selected + after + input.value.substring(end);
    input.focus();
    input.selectionStart = start + before.length;
    input.selectionEnd = start + before.length + selected.length;
    updatePreview();
  };

  function formatBold() { insertAtCursor('**', '**'); }
  function formatItalic() { insertAtCursor('*', '*'); }
  function formatH3() { insertAtCursor('### ', ''); }
  function formatH4() { insertAtCursor('#### ', ''); }
  function insertQuote() { insertAtCursor('> ', ''); }

  function insertLink() {
    const url = prompt("Link URL:");
    if (url) insertAtCursor('[Tekst]', '(' + url + ')');
  }

  function insertCode() { insertAtCursor('`', '`'); }

  // ==================== MODALS ====================
  function showModal(title, contentHTML) {
    let modal = document.getElementById('nexus-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'nexus-modal';
      modal.style.cssText = `position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:99999;display:flex;align-items:center;justify-content:center;`;
      modal.innerHTML = `
        <div style="background:#1e2937;padding:25px;border-radius:16px;max-width:560px;width:94%;box-shadow:0 10px 40px rgba(0,0,0,0.8);color:white;">
          <div id="modal-header" style="color:#67e8f9;font-size:1.4em;text-align:center;margin-bottom:20px;"></div>
          <div id="modal-body" style="max-height:60vh;overflow-y:auto;"></div>
          <button onclick="closeModal()" style="margin-top:20px;width:100%;padding:14px;background:#334155;border:none;border-radius:12px;color:white;font-size:1.1em;">Sluiten</button>
        </div>`;
      document.body.appendChild(modal);
    }
    document.getElementById('modal-header').textContent = title;
    document.getElementById('modal-body').innerHTML = contentHTML;
    modal.style.display = 'flex';
  }

  window.closeModal = function() {
    const modal = document.getElementById('nexus-modal');
    if (modal) modal.style.display = 'none';
  };

  function showEmojiMenu() {
    const emojis = ['😊','🙂','😌','😉','😎','🤓','🥳','🎉','🔥','💡','🚀','🌍','🛡️','🕊️','👍','❤️','💙','💚','💜','🤍','👏','🙌','💪','🧠','📖','🔗','⚡','🌱','📌','✅','❌','❗','❓','💭','💬','🗣️','👥','🤝','🏛️','⚖️','📊','📈','😂','😍','😢','😠','🤔','🤯','🥺','🙏','✨','⭐','🌟','🏆','🎯','♻️','📜','🔦','☀️','🌙','⚡','🔋','📱','💻','🖥️','📚','🏅','🧩','💰','🌍','🗽','⚖️','🔍','🕵️','🧭','🏛️','📜','🛡️','🌐','🔬','📡','🛰️','📻','📢','🗝️','🔑','🗳️','🕊️','🌿','🌳','🏔️','🏠','🛠️','🔨','📝','✍️','📋','📌','⏳','⌛','🔄','♾️','🧬','🧪','🧩','🧠','📊','📉','📈','💾','☁️'];
    let html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:10px;font-size:2.2em;padding:15px 10px;">';
    emojis.forEach(emoji => {
      html += `<span onclick="insertAtCursor('${emoji}', '');closeModal()" style="cursor:pointer;padding:8px;text-align:center;border-radius:12px;">${emoji}</span>`;
    });
    html += '</div>';
    showModal('Kies een emoji', html);
  }

  function showListMenu() {
    const html = `
      <div style="display:flex;flex-direction:column;gap:14px;padding:20px;">
        <button onclick="insertAtCursor('\\n1. ','');closeModal()" style="padding:18px;font-size:1.1em;background:#334155;color:white;border:none;border-radius:12px;">1. Genummerde lijst</button>
        <button onclick="insertAtCursor('\\n- ','');closeModal()" style="padding:18px;font-size:1.1em;background:#334155;color:white;border:none;border-radius:12px;">2. Bullet lijst (-)</button>
        <button onclick="insertAtCursor('\\n  - ','');closeModal()" style="padding:18px;font-size:1.1em;background:#334155;color:white;border:none;border-radius:12px;">3. Sub-bullet lijst</button>
      </div>`;
    showModal('Kies lijst-type', html);
  }

  // ==================== AUTO-CONTINUE LIJSTEN ====================
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      const cursorPos = input.selectionStart;
      const textBefore = input.value.substring(0, cursorPos);
      const lines = textBefore.split('\n');
      const currentLine = lines[lines.length - 1];

      const bulletMatch = currentLine.match(/^(\s*)([-•]|\d+\.)\s+/);

      if (bulletMatch) {
        const indent = bulletMatch[1];
        const marker = bulletMatch[2];

        e.preventDefault();

        if (currentLine.trim() === marker || currentLine.trim() === '') {
          let newText = textBefore.substring(0, textBefore.lastIndexOf('\n') + 1);
          newText += '\n';
          input.value = newText + input.value.substring(cursorPos);
          input.selectionStart = input.selectionEnd = newText.length;
        } else {
          let newLine = '\n' + indent;
          if (marker.match(/^\d+\.$/)) {
            const num = parseInt(marker) + 1;
            newLine += num + '. ';
          } else {
            newLine += marker + ' ';
          }
          input.value = textBefore + newLine + input.value.substring(cursorPos);
          input.selectionStart = input.selectionEnd = textBefore.length + newLine.length;
        }
        updatePreview();
      }
    }
  });

  function insertAtCursor(before, after) {
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const selectedText = input.value.substring(start, end);
    const newText = before + selectedText + after;

    input.value = input.value.substring(0, start) + newText + input.value.substring(end);
    input.focus();
    input.selectionStart = start + before.length;
    input.selectionEnd = start + before.length + selectedText.length;
    updatePreview();
  }

  // ==================== PREVIEW ====================
  function updatePreview() {
    let text = input.value || "Je post verschijnt hier...";

    let html = text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/^### (.*$)/gm, '<h3 style="color:#1e40af; margin:1.8em 0 0.6em 0; font-weight:700;">📌 $1</h3>')
      .replace(/^#### (.*$)/gm, '<h4 style="color:#1e40af; margin:1.5em 0 0.5em 0; font-weight:700;">🔹 $1</h4>')
      .replace(/^>\s?(.*)$/gm, '<span style="color:#22d3ee;">💬</span> <em>$1</em>')
      .replace(/`(.+?)`/g, '<code style="font-family:monospace;background:#2a2f38;padding:3px 7px;border-radius:6px;color:#e0e0e0;">$1</code>')
      .replace(/\n/g, '<br>');

    preview.innerHTML = html;
  }

  // ==================== HASH FUNCTIONS ====================
  function normalizeForHash(text) {
    return text
      .toLowerCase()
      .replace(/[\*\_\`\~\#\>\-\|\•\s\n\r\t]+/g, ' ')
      .replace(/[^\p{L}\p{N}\p{P}\p{S}]/gu, '')
      .trim();
  }

  async function calculateSHA256(text) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  async function updateHash() {
    const rawText = input.value.trim();
    if (!rawText) {
      document.getElementById('hash-signature').style.display = 'none';
      return;
    }

    const unicodeText = convertToUnicode(rawText);
    const fullHash = await calculateSHA256(unicodeText);
    const clean = normalizeForHash(rawText);
    const cleanHash = await calculateSHA256(clean);

    document.getElementById('hash-value').innerHTML = `
      <strong>SHA256 (volledige post):</strong> ${fullHash}<br><br>
      <strong>Clean SHA256:</strong> ${cleanHash}
    `;

    document.getElementById('hash-signature').style.display = 'block';
  }

  // ==================== COPY FUNCTIONS ====================
  async function copyWithSignature(type) {
    let content = input.value.trim();
    if (!content) return;

    const includeHash = document.getElementById('include-hash').checked;
    let finalText = convertToUnicode(content);

    if (includeHash) {
      const clean = normalizeForHash(content);
      const cleanHash = await calculateSHA256(clean);

      const signature = `\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 #OIM × Nexus Quick Post
Geverifieerd via openinternetmanifest.org

Clean SHA256: ${cleanHash}

→ Verifiëren: https://openinternetmanifest.org/nl/hash-verifier
━━━━━━━━━━━━━━━━━━━━━━━━━━━━`;

      finalText += signature;
    }

    navigator.clipboard.writeText(finalText).then(() => {
      if (type === 'facebook') {
        alert("✅ Gekopieerd voor Facebook!");
        window.open('https://www.facebook.com', '_blank');
      } else if (type === 'unicode') {
        alert("✅ Pure Unicode versie gekopieerd!");
      } else if (type === 'x') {
        alert("✅ Gekopieerd voor X/Twitter!");
        window.open('https://x.com', '_blank');
      }
    });
  }

  function copyForFacebook() { copyWithSignature('facebook'); }
  function copyUnicodeWithSignature() { copyWithSignature('unicode'); }
  function copyForX() { copyWithSignature('x'); }
  function copyUnicodeNoSignature() {
    const text = convertToUnicode(input.value.trim());
    navigator.clipboard.writeText(text).then(() => {
      alert("✅ Pure Unicode versie (zonder handtekening) gekopieerd!");
    });
  }

  async function submitForVerification() {
    const text = input.value.trim();
    if (!text) return;

    const fullHash = await calculateSHA256(convertToUnicode(text));
    const clean = normalizeForHash(text);
    const cleanHash = await calculateSHA256(clean);

    const issueTitle = encodeURIComponent("Nexus Quick Post - Verificatie verzoek");
    const issueBody = encodeURIComponent(`**Post tekst:**\n\n${text}\n\n**SHA256 (volledige post):** ${fullHash}\n**Clean SHA256:** ${cleanHash}\n\nAutomatisch ingediend via Nexus Quick Post.`);

    const url = `https://github.com/OpenInternetManifest/Open_Internet_Manifest/issues/new?title=${issueTitle}&body=${issueBody}&labels=quick-post,verification`;
    window.open(url, '_blank');
  }

  // ==================== EVENT LISTENERS ====================
  input.addEventListener('input', () => {
    updatePreview();
    autoResize();
    updateHash();
  });

  function autoResize() {
    input.style.height = 'auto';
    input.style.height = input.scrollHeight + 'px';
  }

  autoResize();
  updatePreview();
  updateHash();

</script>