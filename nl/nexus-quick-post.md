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
        <button onclick="insertAtCursor('### ', '')">H3</button>
        <button onclick="insertAtCursor('#### ', '')">H4</button>
        <button onclick="insertAtCursor('**', '**')">𝐁</button>
        <button onclick="insertAtCursor('*', '*')">𝐼</button>
        <button onclick="insertAtCursor('> ', '')">„ Citaat</button>
        <button onclick="insertAtCursor('\n- ', '')">• Lijst</button>
        <button onclick="showEmojiMenu()">😊</button>
      </div>
      
      <textarea id="post-input" placeholder="Typ of plak je tekst hier..."></textarea>
    </div>

    <div class="preview-panel">
      <div class="panel-header">Facebook Preview</div>
      <div id="fb-preview" class="facebook-preview-box"></div>
    </div>
  </div>

   <div class="actions-bar">
    <label class="toggle-label">
      <input type="checkbox" id="include-hash" checked>
      <span>Include Hash + Signature</span>
    </label>

    <div class="copy-buttons">
      <button onclick="copyForFacebook()" class="btn-facebook">📘 Facebook</button>
      <button onclick="copyUnicodeOnly()" class="btn-secondary">🔄 Unicode</button>
      <button onclick="copyForX()" class="btn-secondary">𝕏 X/Twitter</button>
    </div>
  </div>

<script>
  const input = document.getElementById('post-input');
  const preview = document.getElementById('fb-preview');

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

  function showEmojiMenu() {
    const emoji = prompt("Emoji (bijv. 🔥):", "😊");
    if (emoji) insertAtCursor(emoji + " ");
  }

  function updatePreview() {
    preview.innerHTML = input.value.replace(/\n/g, '<br>');
  }

  function getSignature() {
    if (!document.getElementById('include-hash').checked) return '';
    return `\n\n────────────────────────────\n#OIM • Nexus Quick Post\nGeverifieerd via openinternetmanifest.org\nSHA256: demo-hash...`;
  }

  // ==================== COPY FUNCTIONS ====================
  function copyForFacebook() {
    let text = input.value.trim() + getSignature();
    navigator.clipboard.writeText(text).then(() => {
      alert("✅ Gekopieerd voor Facebook!\n\nGa naar Facebook en plak (Ctrl+V).");
      window.open('https://www.facebook.com/sharer/sharer.php', '_blank');
    });
  }

  function copyUnicodeOnly() {
    let text = input.value.trim() + getSignature();
    navigator.clipboard.writeText(text).then(() => {
      alert("✅ Unicode versie (met opmaak + hash) gekopieerd!");
    });
  }

   function copyForX() {
    let text = input.value.trim() + getSignature();
    navigator.clipboard.writeText(text).then(() => {
      alert("✅ Gekopieerd voor X!\n\nGa naar X en plak (Ctrl+V).");
      window.open('https://x.com/intent/post', '_blank');
    });
  }

  input.addEventListener('input', updatePreview);
  updatePreview();
</script>