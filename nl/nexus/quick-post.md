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

  // ==================== CENTRALE UNICODE CONVERTER ====================
  function convertToUnicode(text) {
    let result = text;

    // Bold
    result = result.replace(/\*\*(.+?)\*\*/g, (match, p1) => p1.split('').map(c => {
      const m = {'a':'𝐚','b':'𝐛','c':'𝐜','d':'𝐝','e':'𝐞','f':'𝐟','g':'𝐠','h':'𝐡','i':'𝐢',
                 'j':'𝐣','k':'𝐤','l':'𝐥','m':'𝐦','n':'𝐧','o':'𝐨','p':'𝐩','q':'𝐪','r':'𝐫',
                 's':'𝐬','t':'𝐭','u':'𝐮','v':'𝐯','w':'𝐰','x':'𝐱','y':'𝐲','z':'𝐳',
                 'A':'𝐀','B':'𝐁','C':'𝐂','D':'𝐃','E':'𝐄','F':'𝐅','G':'𝐆','H':'𝐇','I':'𝐈',
                 'J':'𝐉','K':'𝐊','L':'𝐋','M':'𝐌','N':'𝐍','O':'𝐎','P':'𝐏','Q':'𝐐','R':'𝐑',
                 'S':'𝐒','T':'𝐓','U':'𝐔','V':'𝐕','W':'𝐖','X':'𝐗','Y':'𝐘','Z':'𝐙'};
      return m[c] || c;
    }).join(''));

    // Italic
    result = result.replace(/\*(.+?)\*/g, (match, p1) => p1.split('').map(c => {
      const m = {'a':'𝘢','b':'𝘣','c':'𝘤','d':'𝘥','e':'𝘦','f':'𝘧','g':'𝘨','h':'𝘩','i':'𝘪',
                 'j':'𝘫','k':'𝘬','l':'𝘭','m':'𝘮','n':'𝘯','o':'𝘰','p':'𝘱','q':'𝘲','r':'𝘳',
                 's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻',
                 'A':'𝘈','B':'𝘉','C':'𝘊','D':'𝘋','E':'𝘌','F':'𝘍','G':'𝘎','H':'𝘏','I':'𝘐',
                 'J':'𝘑','K':'𝘒','L':'𝘓','M':'𝘔','N':'𝘕','O':'𝘖','P':'𝘗','Q':'𝘘','R':'𝘙',
                 'S':'𝘚','T':'𝘛','U':'𝘜','V':'𝘝','W':'𝘞','X':'𝘟','Y':'𝘠','Z':'𝘡'};
      return m[c] || c;
    }).join(''));

       // Headers met duidelijk Unicode font + emoji (blijft in copy)
    result = result.replace(/^### (.*$)/gm, (match, p1) => {
      const bold = p1.split('').map(c => {
        const m = {'a':'𝐚','b':'𝐛','c':'𝐜','d':'𝐝','e':'𝐞','f':'𝐟','g':'𝐠','h':'𝐡','i':'𝐢',
                   'j':'𝐣','k':'𝐤','l':'𝐥','m':'𝐦','n':'𝐧','o':'𝐨','p':'𝐩','q':'𝐪','r':'𝐫',
                   's':'𝐬','t':'𝐭','u':'𝐮','v':'𝐯','w':'𝐰','x':'𝐱','y':'𝐲','z':'𝐳',
                   'A':'𝐀','B':'𝐁','C':'𝐂','D':'𝐃','E':'𝐄','F':'𝐅','G':'𝐆','H':'𝐇','I':'𝐈',
                   'J':'𝐉','K':'𝐊','L':'𝐋','M':'𝐌','N':'𝐍','O':'𝐎','P':'𝐏','Q':'𝐐','R':'𝐑',
                   'S':'𝐒','T':'𝐓','U':'𝐔','V':'𝐕','W':'𝐖','X':'𝐗','Y':'𝐘','Z':'𝐙'};
        return m[c] || c;
      }).join('');
      return `📌 ${bold}`;
    });

    result = result.replace(/^#### (.*$)/gm, (match, p1) => {
      const bold = p1.split('').map(c => {
        const m = {'a':'𝗮','b':'𝗯','c':'𝗰','d':'𝗱','e':'𝗲','f':'𝗳','g':'𝗴','h':'𝗵','i':'𝗶',
                   'j':'𝗷','k':'𝗸','l':'𝗹','m':'𝗺','n':'𝗻','o':'𝗼','p':'𝗽','q':'𝗾','r':'𝗿',
                   's':'𝘀','t':'𝘁','u':'𝘂','v':'𝘃','w':'𝘄','x':'𝘅','y':'𝘆','z':'𝘇',
                   'A':'𝗔','B':'𝗕','C':'𝗖','D':'𝗗','E':'𝗘','F':'𝗙','G':'𝗚','H':'𝗛','I':'𝗜',
                   'J':'𝗝','K':'𝗞','L':'𝗟','M':'𝗠','N':'𝗡','O':'𝗢','P':'𝗣','Q':'𝗤','R':'𝗥',
                   'S':'𝗦','T':'𝗧','U':'𝗨','V':'𝗩','W':'𝗪','X':'𝗫','Y':'𝗬','Z':'𝗭'};
        return m[c] || c;
      }).join('');
      return `🔹 ${bold}`;
      });

    // Blockquote
    result = result.replace(/^>\s?(.*)$/gm, (match, p1) => {
      const italic = p1.trim().split('').map(c => {
        const m = {'a':'𝘢','b':'𝘣','c':'𝘤','d':'𝘥','e':'𝘦','f':'𝘧','g':'𝘨','h':'𝘩','i':'𝘪',
                   'j':'𝘫','k':'𝘬','l':'𝘭','m':'𝘮','n':'𝘯','o':'𝘰','p':'𝘱','q':'𝘲','r':'𝘳',
                   's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻',
                   'A':'𝘈','B':'𝘉','C':'𝘊','D':'𝘋','E':'𝘌','F':'𝘍','G':'𝘎','H':'𝘏','I':'𝘐',
                   'J':'𝘑','K':'𝘒','L':'𝘓','M':'𝘔','N':'𝘕','O':'𝘖','P':'𝘗','Q':'𝘘','R':'𝘙',
                   'S':'𝘚','T':'𝘛','U':'𝘜','V':'𝘝','W':'𝘞','X':'𝘟','Y':'𝘠','Z':'𝘡'};
        return m[c] || c;
      }).join('');
      return `💬 ${italic}`;
    });

    // Inline code
    result = result.replace(/`(.+?)`/g, (match, p1) => {
      const mono = p1.split('').map(c => {
        const m = {'a':'𝚊','b':'𝚋','c':'𝚌','d':'𝚍','e':'𝚎','f':'𝚏','g':'𝚐','h':'𝚑','i':'𝚒',
                   'j':'𝚓','k':'𝚔','l':'𝚕','m':'𝚖','n':'𝚗','o':'𝚘','p':'𝚙','q':'𝚚','r':'𝚛',
                   's':'𝚜','t':'𝚝','u':'𝚞','v':'𝚟','w':'𝚠','x':'𝚡','y':'𝚢','z':'𝚣',
                   'A':'𝙰','B':'𝙱','C':'𝙲','D':'𝙳','E':'𝙴','F':'𝙵','G':'𝙶','H':'𝙷','I':'𝙸',
                   'J':'𝙹','K':'𝙺','L':'𝙻','M':'𝙼','N':'𝙽','O':'𝙾','P':'𝙿','Q':'𝚀','R':'𝚁',
                   'S':'𝚂','T':'𝚃','U':'𝚄','V':'𝚅','W':'𝚆','X':'𝚇','Y':'𝚈','Z':'𝚉',
                   '0':'𝟶','1':'𝟷','2':'𝟸','3':'𝟹','4':'𝟺','5':'𝟻','6':'𝟼','7':'𝟽','8':'𝟾','9':'𝟿'};
        return m[c] || c;
      }).join('');
      return '`' + mono + '`';
    });

    return result;
  }
 // ==================== AUTO-CONTINUE LIJSTEN (met extra witregel) ====================
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
        // Lege bullet → verwijder bullet + voeg extra witregel toe
        let newText = textBefore.substring(0, textBefore.lastIndexOf('\n') + 1);
        
        // Extra lege regel toevoegen
        newText += '\n';

        input.value = newText + input.value.substring(cursorPos);
        input.selectionStart = input.selectionEnd = newText.length;
      } else {
        // Nieuwe lijstregel aanmaken
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

  // ==================== PREVIEW (exact match met copy - GEEN underline) ====================
  function updatePreview() {
    let text = input.value || "Je post verschijnt hier...";

    let html = text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')

      // Headers - EXACT dezelfde weergave als copy (GEEN underline!)
      .replace(/^### (.*$)/gm, '<h3 style="color:#1e40af; margin:1.8em 0 0.6em 0; font-weight:700;">📌 $1</h3>')
      .replace(/^#### (.*$)/gm, '<h4 style="color:#1e40af; margin:1.5em 0 0.5em 0; font-weight:700;">🔹 $1</h4>')

       // Blockquote
      .replace(/^>\s?(.*)$/gm, '<span style="color:#22d3ee;">💬</span> <em>$1</em>')

      // Inline code
      .replace(/`(.+?)`/g, '<code style="font-family:monospace;background:#2a2f38;padding:3px 7px;border-radius:6px;color:#e0e0e0;">$1</code>')

      .replace(/\n/g, '<br>');

    preview.innerHTML = html;
  }

// ==================== HASH FUNCTIONS ====================

// Normalisatie voor clean hash (voor verifier + prob check)
function normalizeForHash(text) {
  return text
    .toLowerCase()
    .replace(/[\*\_\`\~\#\>\-\|\•\•\s\n\r\t]+/g, ' ')
    .replace(/[^\p{L}\p{N}\p{P}\p{S}]/gu, '')
    .trim();
}

// SHA256 berekenen
async function calculateSHA256(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Live hash updaten (beide hashes tonen)
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
  // Submit voor verificatie (GitHub Issue)
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

→ Beste verificatie:
   Plak de volledige post (inclusief deze handtekening) in:
   https://openinternetmanifest.org/nl/hash-verifier

→ Handmatig checken:
   Gebruik alleen de tekst bóven deze streep in een online SHA256 tool
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
// ==================== COPY FUNCTIONS ====================

function copyForFacebook() {
  copyWithSignature('facebook');
}

function copyUnicodeWithSignature() {
  copyWithSignature('unicode');
}

function copyForX() {
  copyWithSignature('x');
}

function copyUnicodeNoSignature() {
  const text = convertToUnicode(input.value.trim());
  navigator.clipboard.writeText(text).then(() => {
    alert("✅ Pure Unicode versie (zonder handtekening) gekopieerd!");
  });
}

  // Event listeners
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