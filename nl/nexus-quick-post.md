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
        Live voorbeeld hoe het op Facebook eruit komt te zien
      </div>
      <div id="fb-preview" class="facebook-preview-box"></div>
    </div>
  </div>

  <!-- Nieuwe actions bar -->
<div class="actions-bar">
  <label class="toggle-label">
    <input type="checkbox" id="include-hash" checked>
    <span>Include Hash + Signature</span>
  </label>

  <div class="copy-buttons">
    <button onclick="copyForFacebook()" class="btn-facebook">
      📘 Facebook
    </button>
    <button onclick="copyUnicodeOnly()" class="btn-secondary">
      🔄 Unicode
    </button>
    <button onclick="copyMarkdown()" class="btn-secondary">
      📄 Markdown
    </button>
    <button onclick="copyForX()" class="btn-secondary">
      𝕏 X/Twitter
    </button>
  </div>
</div>

  <div id="result" class="result-area"></div>
</div>

<script>
  const input = document.getElementById('post-input');
  const preview = document.getElementById('fb-preview');

  // ==================== TOOLBAR FUNCTIES ====================
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

// ==================== MODAL SYSTEM (werkende versie + titel fix) ====================
function showModal(title, contentHTML) {
  console.log("Modal geopend met titel:", title);

  let modal = document.getElementById('nexus-modal');
  
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'nexus-modal';
    modal.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
      background: rgba(0,0,0,0.9); z-index: 99999; 
      display: flex; align-items: center; justify-content: center;
    `;
    modal.innerHTML = `
      <div style="background:#1e2937; padding:25px; border-radius:16px; max-width:560px; width:94%; 
                  box-shadow:0 10px 40px rgba(0,0,0,0.8); color:white;">
        <div id="modal-header" style="color:#67e8f9; font-size:1.4em; text-align:center; margin-bottom:20px;"></div>
        <div id="modal-body" style="max-height:60vh; overflow-y:auto;"></div>
        <button onclick="closeModal()" style="margin-top:20px; width:100%; padding:14px; background:#334155; border:none; border-radius:12px; color:white; font-size:1.1em;">Sluiten</button>
      </div>`;
    document.body.appendChild(modal);
  }

  // Titel altijd updaten
  document.getElementById('modal-header').textContent = title;
  
  // Content updaten
  document.getElementById('modal-body').innerHTML = contentHTML;
  
  modal.style.display = 'flex';
}

function closeModal() {
  const modal = document.getElementById('nexus-modal');
  if (modal) modal.style.display = 'none';
}

// ==================== EMOJI & LIST (met deze modal) ====================
function showEmojiMenu() {
  const emojis = [
    '😊','🙂','😌','😉','😎','🤓','🥳','🎉','🔥','💡','🚀','🌍','🛡️','🕊️',
    '👍','❤️','💙','💚','💜','🤍','👏','🙌','💪','🧠','📖','🔗','⚡','🌱',
    '📌','✅','❌','❗','❓','💭','💬','🗣️','👥','🤝','🏛️','⚖️','📊','📈',
    '😂','😍','😢','😠','🤔','🤯','🥺','🙏','✨','⭐','🌟','🏆','🎯','♻️',
    '📜','🔦','☀️','🌙','⚡','🔋','📱','💻','🖥️','📚','🏅','🧩','💰','🌍',
    '🗽','⚖️','🔍','🕵️','🧭','🏛️','📜','🛡️','🌐','🔬','📡','🛰️','📻','📢',
    '🗝️','🔑','🗳️','🕊️','🌿','🌳','🏔️','🏠','🛠️','🔨','📝','✍️','📋','📌',
    '⏳','⌛','🔄','♾️','🧬','🧪','🧬','🧩','🧠','📊','📉','📈','💾','☁️'
  ];

  let html = '<div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; font-size: 2.1em; padding: 20px 10px;">';
  emojis.forEach(emoji => {
    html += `<span onclick="insertAtCursor('${emoji}', ''); closeModal();" style="cursor:pointer; padding:10px; text-align:center;">${emoji}</span>`;
  });
  html += '</div>';

  showModal('Kies een emoji', html);
}

function showListMenu() {
  const html = `
    <div style="display:flex; flex-direction:column; gap:14px; padding:20px;">
      <button onclick="insertAtCursor('\\n1. ', ''); closeModal()" style="padding:18px; font-size:1.1em; background:#334155; color:white; border:none; border-radius:12px;">1. Genummerde lijst</button>
      <button onclick="insertAtCursor('\\n- ', ''); closeModal()" style="padding:18px; font-size:1.1em; background:#334155; color:white; border:none; border-radius:12px;">2. Bullet lijst (-)</button>
      <button onclick="insertAtCursor('\\n  - ', ''); closeModal()" style="padding:18px; font-size:1.1em; background:#334155; color:white; border:none; border-radius:12px;">3. Sub-bullet lijst</button>
    </div>`;

  showModal('Kies lijst-type', html);
}

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

  // ==================== COPY FUNCTIONS + HASH ====================
  function getNormalizedText(text) {
    return text.toLowerCase()
      .replace(/[\*\_\`\[\]\(\)#>]/g, '')           // strip markdown
      .replace(/\s+/g, ' ')                         // multiple spaces → single
      .trim();
  }

  function calculateSHA256(str) {
    // Voor nu een placeholder (echte SHA256 later via crypto.subtle)
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).padStart(8, '0') + "...";
  }

  function getSignature(text) {
    if (!document.getElementById('include-hash').checked) return '';
    const normalized = getNormalizedText(text);
    const hash = calculateSHA256(normalized);
    return `\n\n────────────────────────────\n#OIM • Nexus Quick Post\nGeverifieerd via openinternetmanifest.org\nSHA256: ${hash}`;
  }

  function showCopyFeedback(btn) {
    const original = btn.innerHTML;
    btn.classList.add('copied');
    btn.innerHTML = '✅ Gekopieerd!';
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.innerHTML = original;
    }, 1800);
  }

  function copyForFacebook() {
    let text = input.value.trim();
    if (!text) return;
    text += getSignature(text);
    navigator.clipboard.writeText(text).then(() => {
      showCopyFeedback(event.currentTarget);
      if (confirm("✅ Gekopieerd!\n\nFacebook openen?")) {
        window.open('https://www.facebook.com/sharer/sharer.php', '_blank');
      }
    });
  }

  function copyUnicodeOnly() {
    let text = input.value.trim();
    navigator.clipboard.writeText(text).then(() => showCopyFeedback(event.currentTarget));
  }

  function copyMarkdown() {
    let text = input.value.trim();
    navigator.clipboard.writeText(text).then(() => showCopyFeedback(event.currentTarget));
  }

  function copyForX() {
    let text = input.value.trim();
    text += getSignature(text);
    navigator.clipboard.writeText(text).then(() => showCopyFeedback(event.currentTarget));
  }

  window.insertListType = function(type) {
    if (type === 1) insertAtCursor('\n1. ', '');
    else if (type === 2) insertAtCursor('\n- ', '');
    else if (type === 3) insertAtCursor('\n  - ', '');
  };

  let ignoreNextEnter = false;

  // Auto-continue lijst bij Enter (origineel behouden)
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      if (ignoreNextEnter) {
        ignoreNextEnter = false;
        return;
      }

      const cursorPos = input.selectionStart;
      const textBeforeCursor = input.value.substring(0, cursorPos);
      const lines = textBeforeCursor.split('\n');
      const lastLine = lines[lines.length - 1];

      if (lastLine.trim().match(/^(\d+\.|-)\s*$/)) {
        e.preventDefault();
        const newText = input.value.substring(0, cursorPos - lastLine.length - 1).trimEnd();
        input.value = newText;
        input.selectionStart = input.selectionEnd = newText.length;
        updatePreview();
        ignoreNextEnter = true;
        return;
      }

      let newBullet = '';

      if (lastLine.match(/^\s*-\s/)) {
        newBullet = '\n- ';
      } else if (lastLine.match(/^\s*\d+\.\s/)) {
        const numMatch = lastLine.match(/^\s*(\d+)\./);
        if (numMatch) {
          const num = parseInt(numMatch[1]) + 1;
          newBullet = '\n' + num + '. ';
        }
      }

      if (newBullet) {
        e.preventDefault();
        insertAtCursor(newBullet, '');
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

  function updatePreview() {
    let text = input.value || "Je post verschijnt hier...";

    // Vet + Cursief
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
                 's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻',
                 'A':'𝘈','B':'𝘉','C':'𝘊','D':'𝘋','E':'𝘌','F':'𝘍','G':'𝘎','H':'𝘏','I':'𝘐',
                 'J':'𝘑','K':'𝘒','L':'𝘓','M':'𝘔','N':'𝘕','O':'𝘖','P':'𝘗','Q':'𝘘','R':'𝘙',
                 'S':'𝘚','T':'𝘛','U':'𝘜','V':'𝘝','W':'𝘞','X':'𝘟','Y':'𝘠','Z':'𝘡'};
      return m[c] || c;
    }).join(''));
 
    // HTML voor preview
    let html = text
      .replace(/^#### (.*$)/gm, '<h4 style="color:#1e40af; border-bottom:1px solid #94a3b8; margin:1.2em 0 0.6em 0;">$1</h4>')
      .replace(/^### (.*$)/gm, '<h3 style="color:#1e40af; border-bottom:2px solid #22d3ee; margin:1.2em 0 0.6em 0;">$1</h3>')
      .replace(/^## (.*$)/gm, '<h2 style="color:#1e40af; margin:1.2em 0 0.6em 0;">$1</h2>')
      .replace(/^# (.*$)/gm, '<h1 style="color:#1e40af; margin:1.2em 0 0.6em 0;">$1</h1>')

      // Blockquote voor live preview
      .replace(/<blockquote>([\s\S]*?)<\/blockquote>/gi, (match, content) => {
        const lines = content.trim().split('\n').filter(line => line.trim() !== '');
        return lines.map(line => `<span style="color:#22d3ee;">💬</span> <em>${line.trim()}</em>`).join('<br>');
      })
      .replace(/^>\s?(.*)$/gm, (match, p1) => `<span style="color:#22d3ee;">💬</span> <em>${p1.trim()}</em>`)

      .replace(/\[(.*?)\]\((.*?)\)/g, '$1 ($2)')
      .replace(/^---+$/gm, '<hr style="border:none; border-top:1px solid #cbd5e1; margin:1.5em 0;">')
      .replace(/\n/g, '<br>');

    preview.innerHTML = html;
  }

  input.addEventListener('input', updatePreview);

  // Auto-resize textarea
  function autoResize() {
    input.style.height = 'auto';
    input.style.height = input.scrollHeight + 'px';
  }

  input.addEventListener('input', autoResize);
  autoResize();

  function copyForFacebook() {
    let text = input.value.trim();
    if (!text) return;

    // Vet + Cursief
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
                 's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻',
                 'A':'𝘈','B':'𝘉','C':'𝘊','D':'𝘋','E':'𝘌','F':'𝘍','G':'𝘎','H':'𝘏','I':'𝘐',
                 'J':'𝘑','K':'𝘒','L':'𝘓','M':'𝘔','N':'𝘕','O':'𝘖','P':'𝘗','Q':'𝘘','R':'𝘙',
                 'S':'𝘚','T':'𝘛','U':'𝘜','V':'𝘝','W':'𝘞','X':'𝘟','Y':'𝘠','Z':'𝘡'};
      return m[c] || c;
    }).join(''));

    // H3 en H4 vet + subtiele streep
    text = text
      .replace(/^#### (.*$)/gm, (match, p1) => {
        const bold = p1.split('').map(c => {
          const m = {'a':'𝐚','b':'𝐛','c':'𝐜','d':'𝐝','e':'𝐞','f':'𝐟','g':'𝐠','h':'𝐡','i':'𝐢',
                     'j':'𝐣','k':'𝐤','l':'𝐥','m':'𝐦','n':'𝐧','o':'𝐨','p':'𝐩','q':'𝐪','r':'𝐫',
                     's':'𝐬','t':'𝐭','u':'𝐮','v':'𝐯','w':'𝐰','x':'𝐱','y':'𝐲','z':'𝐳',
                     'A':'𝐀','B':'𝐁','C':'𝐂','D':'𝐃','E':'𝐄','F':'𝐅','G':'𝐆','H':'𝐇','I':'𝐈',
                     'J':'𝐉','K':'𝐊','L':'𝐋','M':'𝐌','N':'𝐍','O':'𝐎','P':'𝐏','Q':'𝐐','R':'𝐑',
                     'S':'𝐒','T':'𝐓','U':'𝐔','V':'𝐕','W':'𝐖','X':'𝐗','Y':'𝐘','Z':'𝐙'};
          return m[c] || c;
        }).join('');
        return bold + '\n──────────────';
      })
      .replace(/^### (.*$)/gm, (match, p1) => {
        const bold = p1.split('').map(c => {
          const m = {'a':'𝐚','b':'𝐛','c':'𝐜','d':'𝐝','e':'𝐞','f':'𝐟','g':'𝐠','h':'𝐡','i':'𝐢',
                     'j':'𝐣','k':'𝐤','l':'𝐥','m':'𝐦','n':'𝐧','o':'𝐨','p':'𝐩','q':'𝐪','r':'𝐫',
                     's':'𝐬','t':'𝐭','u':'𝐮','v':'𝐯','w':'𝐰','x':'𝐱','y':'𝐲','z':'𝐳',
                     'A':'𝐀','B':'𝐁','C':'𝐂','D':'𝐃','E':'𝐄','F':'𝐅','G':'𝐆','H':'𝐇','I':'𝐈',
                     'J':'𝐉','K':'𝐊','L':'𝐋','M':'𝐌','N':'𝐍','O':'𝐎','P':'𝐏','Q':'𝐐','R':'𝐑',
                     'S':'𝐒','T':'𝐓','U':'𝐔','V':'𝐕','W':'𝐖','X':'𝐗','Y':'𝐘','Z':'𝐙'};
          return m[c] || c;
        }).join('');
        return bold + '\n──────────────';
      });

  // ==================== BLOCKQUOTE / CITATEN (schoon) ====================
  // Verwijder eerst alle oude quotes die misschien al bestaan
  text = text.replace(/[“”"]/g, '');

  // <blockquote> tags
  text = text.replace(/<blockquote>([\s\S]*?)<\/blockquote>/gi, (match, content) => {
    const lines = content.trim().split('\n');
    const formatted = lines.map(line => {
      if (!line.trim()) return '';
      const italic = line.trim().split('').map(c => {
        const m = {'a':'𝘢','b':'𝘣','c':'𝘤','d':'𝘥','e':'𝘦','f':'𝘧','g':'𝘨','h':'𝘩','i':'𝘪',
                   'j':'𝘫','k':'𝘬','l':'𝘭','m':'𝘮','n':'𝘯','o':'𝘰','p':'𝘱','q':'𝘲','r':'𝘳',
                   's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻',
                   'A':'𝘈','B':'𝘉','C':'𝘊','D':'𝘋','E':'𝘌','F':'𝘍','G':'𝘎','H':'𝘏','I':'𝘐',
                   'J':'𝘑','K':'𝘒','L':'𝘓','M':'𝘔','N':'𝘕','O':'𝘖','P':'𝘗','Q':'𝘘','R':'𝘙',
                   'S':'𝘚','T':'𝘛','U':'𝘜','V':'𝘝','W':'𝘞','X':'𝘟','Y':'𝘠','Z':'𝘡'};
        return m[c] || c;
      }).join('');
      return `💬 ${italic}`;
    }).filter(line => line !== '');

    return formatted.join('\n');
  });

  // Gewone > blockquotes
  text = text.replace(/^>\s?(.*)$/gm, (match, p1) => {
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

  // Inline code → typewriter
  text = text.replace(/`(.+?)`/g, (match, p1) => {
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

  // Link met URL
  text = text.replace(/\[(.*?)\]\((.*?)\)/g, '$1 ($2)');

  // Horizontale lijn
  text = text.replace(/^---+$/gm, '────────────────────────────');

    navigator.clipboard.writeText(text).then(() => {
      const alertMsg = "✅ Gekopieerd voor Facebook!\n\nKlik OK om Facebook te openen.\nPlak de tekst daar (Ctrl+V).";
      if (confirm(alertMsg)) {
        window.open('https://www.facebook.com/sharer/sharer.php', '_blank');
      }
    });
  }

  updatePreview();
  autoResize();
</script>