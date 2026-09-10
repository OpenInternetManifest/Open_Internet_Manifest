document.addEventListener('DOMContentLoaded', function() {

  // ==================== COPY RAW MARKDOWN ====================
  var copyBtn = document.querySelector('.big-copy-btn');
  var copyFeedback = document.getElementById('copy-feedback');

  if (copyBtn && copyFeedback) {
    copyBtn.addEventListener('click', function() {
      var rawEl = document.getElementById('raw-markdown');
      if (rawEl) {
        var rawMarkdown = rawEl.textContent.trim();
        navigator.clipboard.writeText(rawMarkdown).then(() => {
          showFeedback(copyFeedback, '✅ Exacte originele Markdown gekopieerd!', 'success');
          setTimeout(() => { copyFeedback.innerHTML = ''; }, 5000);
        }).catch(() => {
          alert('Copy mislukt.\n\n' + rawMarkdown);
        });
      } else {
        showFeedback(copyFeedback, 'Geen raw_markdown gevonden.', 'warning');
      }
    });
  }

  // ==================== VERIFY BUTTON (full_sha256) ====================
  var verifyBtn = document.getElementById('verify-btn');
  var userHashInput = document.getElementById('user-hash');
  var verifyFeedback = document.getElementById('verify-feedback');

  // Probeer full_sha256 uit hidden input of uit page data
  var officialFullHash = document.getElementById('official-full-hash') 
                       ? document.getElementById('official-full-hash').value.trim() 
                       : (typeof pageFullSha !== 'undefined' ? pageFullSha : null);

  if (verifyBtn && userHashInput && verifyFeedback) {
    verifyBtn.addEventListener('click', function() {
      var userHash = userHashInput.value.trim().toLowerCase();

      if (!userHash) {
        showFeedback(verifyFeedback, 'Plak eerst je SHA256 hash.', 'warning');
        return;
      }
      if (!officialFullHash) {
        showFeedback(verifyFeedback, 'Kan officiële full_sha256 niet vinden op deze pagina.', 'error');
        return;
      }

      if (userHash === officialFullHash.toLowerCase()) {
        showFeedback(verifyFeedback, '✅ 100% MATCH!<br>Exact overeen met de originele Markdown op GitHub.', 'success');
      } else {
        showFeedback(verifyFeedback, '❌ Geen match.<br><br>Jouw hash: ' + userHash + '<br>Officieel: ' + officialFullHash, 'error');
      }
    });

    userHashInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') verifyBtn.click();
    });
  }

  function showFeedback(el, msg, type) {
    el.innerHTML = msg;
    el.style.color = type === 'success' ? '#66ff66' : '#ff6666';
  }
});