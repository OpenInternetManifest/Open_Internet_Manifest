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

  <div class="actions-bar">
    <button onclick="generateHashAndSignature()" class="btn-primary">🔐 Generate Hash + Signature</button>
    <button onclick="copyForFacebook()" class="btn-secondary">📋 Copy for Facebook</button>
  </div>

  <div id="result" class="result-area"></div>
</div>



<script>
  const input = document.getElementById('post-input');
  const preview = document.getElementById('fb-preview');

  // Toolbar functies
  function formatBold() {
    insertAtCursor('**', '**');
  }

  function formatItalic() {
    insertAtCursor('*', '*');
  }

  function formatH3() {
    insertAtCursor('### ', '');
  }

  function formatH4() {
    insertAtCursor('#### ', '');
  }

  function insertQuote() {
    insertAtCursor('> ', '');
  }

  function insertLink() {
    const url = prompt("Link URL:");
    if (url) insertAtCursor('[Tekst]', '(' + url + ')');
  }

  function insertCode() {
    insertAtCursor('`', '`');
  }

  function showListMenu() {
    const message = `Kies lijst type (typ nummer):\n\n` +
                    `1. Genummerd (1. 2. 3.)\n` +
                    `2. Bullet (-)\n` +
                    `3. Sub-bullet (  - )\n\n` +
                    `Typ 1, 2 of 3:`;

    const choice = prompt(message, "1");
    if (choice === "1") insertAtCursor('\n1. ', '');
    else if (choice === "2") insertAtCursor('\n- ', '');
    else if (choice === "3") insertAtCursor('\n  - ', '');
  }

  let ignoreNextEnter = false;

  // Auto-continue lijst bij Enter
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

      function showEmojiMenu() {
    const commonEmojis = ['😊','👍','❤️','🔥','🚀','💡','🌍','🛡️','🎉','📌','✅','❌','😂','😍','🙌','⭐','🌟','💪','🧠','📖','🔗','⚡','🌱','🕊️'];

    let message = "Kies emoji (typ het nummer):\n\n";
    commonEmojis.forEach((emoji, i) => {
      message += `${i+1}. ${emoji}   `;
      if ((i+1) % 6 === 0) message += "\n";
    });

    const choice = prompt(message, "");
    if (choice) {
      const index = parseInt(choice) - 1;
      if (index >= 0 && index < commonEmojis.length) {
        insertAtCursor(commonEmojis[index], '');
      } else {
        // Als gebruiker iets anders typt, neem dat
        insertAtCursor(choice.trim(), '');
      }
    }
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
      .replace(/^> (.*$)/gm, '<blockquote style="border-left:4px solid #22d3ee; padding-left:1em; color:#334155; font-style:italic; margin:1em 0;">“$1”</blockquote>')
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

  // Citaat met aanhalingstekens + cursief
  text = text.replace(/^> (.*$)/gm, (match, p1) => {
    const italic = p1.split('').map(c => {
      const m = {'a':'𝘢','b':'𝘣','c':'𝘤','d':'𝘥','e':'𝘦','f':'𝘧','g':'𝘨','h':'𝘩','i':'𝘪',
                 'j':'𝘫','k':'𝘬','l':'𝘭','m':'𝘮','n':'𝘯','o':'𝘰','p':'𝘱','q':'𝘲','r':'𝘳',
                 's':'𝘴','t':'𝘵','u':'𝘶','v':'𝘷','w':'𝘸','x':'𝘹','y':'𝘺','z':'𝘻',
                 'A':'𝘈','B':'𝘉','C':'𝘊','D':'𝘋','E':'𝘌','F':'𝘍','G':'𝘎','H':'𝘏','I':'𝘐',
                 'J':'𝘑','K':'𝘒','L':'𝘓','M':'𝘔','N':'𝘕','O':'𝘖','P':'𝘗','Q':'𝘘','R':'𝘙',
                 'S':'𝘚','T':'𝘛','U':'𝘜','V':'𝘝','W':'𝘞','X':'𝘟','Y':'𝘠','Z':'𝘡'};
      return m[c] || c;
    }).join('');
    return '“' + italic + '”';
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

  // Auto-resize textarea
  function autoResize() {
    input.style.height = 'auto';
    input.style.height = input.scrollHeight + 'px';
  }

  input.addEventListener('input', () => {
    updatePreview();
    autoResize();
  });

  // Initial resize
  autoResize();
</script>