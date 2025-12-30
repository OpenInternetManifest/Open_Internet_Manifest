function copyPageText() {
  const mainContent = document.querySelector('.main-content');
  if (!mainContent) return;

  const clone = mainContent.cloneNode(true);

  // Verwijder alle includes + footer + credits + navigatie + feedback
  const toRemove = clone.querySelectorAll(
    '.integrity-check, .community-box, .donation-section, .page-footer, .copy-container, #copy-feedback, #verify-feedback, .site-footer, .footer-nav, .site-footer-credits'
  );
  toRemove.forEach(el => el.remove());

  let text = clone.textContent || clone.innerText || '';
  text = text.trim().replace(/\n{3,}/g, '\n\n');

  navigator.clipboard.writeText(text).then(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) {
      const lang = document.documentElement.lang || 'nl';
      const copiedText = lang === 'en' ? '✓ Page text copied!' : '✓ Pagina tekst gekopieerd!';
      feedback.innerHTML = `<span style="color: #66ff66 !important; font-weight: bold;">${copiedText}</span>`;
      setTimeout(() => feedback.innerHTML = '', 3000);
    }
  }).catch(() => {
    const feedback = document.getElementById('copy-feedback');
    if (feedback) {
      const lang = document.documentElement.lang || 'nl';
      const errorText = lang === 'en' ? 'Copy failed – select manually' : 'Copy mislukt – selecteer handmatig';
      feedback.innerHTML = `<span style="color: #ff6666 !important;">${errorText}</span>`;
    }
  });
}

function verifyHash() {
  const userHash = document.getElementById('user-hash').value.trim().toLowerCase();
  if (!userHash) {
    const lang = document.documentElement.lang || 'nl';
    const noHashText = lang === 'en' ? '✗ Enter a hash' : '✗ Voer een hash in';
    document.getElementById('verify-feedback').innerHTML = `<span style="color: #ff6666 !important;">${noHashText}</span>`;
    return;
  }

  let pagePath = window.location.pathname;
  pagePath = pagePath.replace(/\/$/, '').replace(/^\/Open_Internet_Manifest/, '');

  const expectedHash = getExpectedHash(pagePath);

  const feedback = document.getElementById('verify-feedback');
  const lang = document.documentElement.lang || 'nl';

  if (userHash === expectedHash) {
    const matchText = lang === 'en' ? '✓ PERFECT MATCH!' : '✓ PERFECTE MATCH!';
    const authText = lang === 'en' ? 'This page is 100% authentic.' : 'Deze pagina is 100% authentiek.';
    feedback.innerHTML = `<span style="color: #66ff66 !important; font-size: 1.2em; font-weight: bold;">${matchText}</span> ${authText}`;
  } else {
    const noMatchText = lang === 'en' ? '✗ No match' : '✗ Geen match';
    const yourHash = lang === 'en' ? 'Your hash:' : 'Jouw hash:';
    const officialHash = lang === 'en' ? 'Official hash:' : 'Officiële hash:';
    const notFound = lang === 'en' ? 'not found' : 'niet gevonden';
    feedback.innerHTML = `<span style="color: #ff6666 !important; font-weight: bold;">${noMatchText}</span><br>
      <strong>${yourHash}</strong> <code style="word-break: break-all;">${userHash}</code><br>
      <strong>${officialHash}</strong> <code style="word-break: break-all;">${expectedHash || notFound}</code>`;
  }
}

// Map van page paths naar hashes (zonder baseurl en trailing slash)
function getExpectedHash(path) {
  const hashes = {
    // nl/theses
 '/nl/over': 'ca25dd7aa0dd2f6bd6853209bcbbe0df79c056902130dcc73bd56e1d19aead94',
'/nl/theses/thesis-00': '38f0da4922c01e05206f4438efa8ba1ec0826727ac4e9d0b5b45c1f30d467684',
'/nl/theses/thesis-01': '4aa8a37884deb164c85153f32f9b300f3e210fe207ff1bbcd896f0706ab7f9cd',
'/nl/theses/thesis-02': '907c8cde997e3ecb894ba92a6b231ee2d85fbc07c636ea27254f62627505ae76',
'/nl/theses/thesis-03': '316a9394652da4fc9ec6611d65a197951018e60ace82e05685ceab73614d21fd',
'/nl/theses/thesis-04': '2c12b7974db54c5aa7961d4f0deb4a6c1b811f3d0ef6aa0ccc938eb9d0f59bf5',
'/nl/theses/thesis-05': '315635ca2cde2ce3f16414a26d57d72a5bec9e3635801f7f721529b069efdeed',
'/nl/theses/thesis-06': '6c4dceb3239f2c5454033c8128eb2dc84d10be39e55c65e3b7b5f136b5517714',
'/nl/theses/thesis-07': '17891a9292077a558b475949128576ebaa8cbcc43a1922eb6559cc8aba0cb408',
'/nl/theses/thesis-08': '167ebd7fcf212d3f1df2960c716c491f4ca1e923473042648a77aef4d1674dec',
'/nl/theses/thesis-09': '0bc38d070ab3932dcdc3687cde9d09f5f1b0ce60d8a213517ca5ed5ac6d9eabd',
'/nl/theses/thesis-10': 'c306a0959d0fe7e37c83e1be84d0d5b439ed0c32706ad3b19c1394c069a6635b',
'/nl/theses/thesis-11': 'a18663438532cc9f2abd3901cfedd7f1a5f60df3b4396724fc1f2ae7fde48580',
'/nl/theses/thesis-12': 'acbb9fe753a6c6a6dbb306841d5e9906bb1651e9a9111210b6c476112cb3722b',
'/nl/theses/thesis-13': '6948dd2316b4828aa248ae57e411aad0dd03059c73c06a22874fe8e8388e3b09',
'/nl/theses/thesis-14': '1cf6993d5e6ba03b67968951baca62c54c67a666c9a649c153316834c4c45aa5',
'/nl/theses/thesis-15': 'd9b48e8d8f1d0e0afde41bf19492eca918085099e26daeb6e8ef3613c6934e7b',
'/nl/theses/thesis-16': 'a2824502f8b25bec3a2fd5b8084f0744bfbdcff0d7326e3a04ef8d4f4787dbee',
'/nl/theses/thesis-17': '3773e19c82caf7fa28d7d3dcd92cf62e87c014372545b1505d5f6c93ef91214e',
'/nl/theses/thesis-18': '962bb0ae3900251d7f0fc05693783824c229f5d530762d974c24677e9111a8d4',
'/nl/theses/thesis-19': '7a5ec50ba39994edaec0aaf3d67028b78d8cbcadf71bd609c41b43d5ca4b936b',
'/nl/theses/thesis-20': '436973094699830c1b0dc37ac8f7e0e8ab46ea6d136523caccbaf0a24a645514',
'/nl/theses/thesis-21': '8c949a9297831b7a5a707e1dfc6f0ef1c0320d05b38dca5da174b7f8dfc735f3',
'/nl/theses/thesis-22': '5aafcad08ab3c28b30b1516b780d645c757b460bb3be49fd6a89d841b4c4f673',
'/nl/theses/thesis-23': 'a592d8d88fe2c0a6625622eba3a88e10fc73126a5208dc940b9307a302cc0dd1',
'/nl/theses/thesis-24': '9ae9da7b6e6961f92e55aaecfc0917cb60b5713fed100c47b6eb8e3343a2e0af',
'/nl/theses/thesis-25': '2c2ccad3c4e9ab00a111775d47353fb44f406b2d235a6663cdbeb06f553e1967',
'/nl/theses/thesis-26': '040d07457fef97f9355fff73a21fb54b60eed07f1adc9e0b1be212d03d1b3f77',
'/nl/theses/thesis-27': '9ccc3939ff52f54ce3ec2f83c8d6871e3354b8d65da6bc74842252a0ef90c5d2',
'/nl/theses/thesis-28': 'c74ce9aea3a3e6f39433a4655e05a4c9027c87b2a3270e0f2cc4659cf059a7b8',
'/nl/theses/thesis-29': '4653ecfe8ed9fd692a171559bd0a260e07fb923fff7236f942e86866c6f97eb5',
'/nl/theses/thesis-30': '26696490d42a972e43e744cf57926306481187ea9d4ea65259a099a646f170e3',
'/nl/theses/levend-manifest': 'c0caf10526d4b5d580ef575721f9f5b258ecd58fba2274fb2e76f698de5e89e8',
// en/theses
'/en/about': 'b0f0a88c94cf17eb46894ada3e4779d960d52c4417209cf7fbdd4a3010da9443',
'/en/theses/thesis-00': '793e85f65f8c680e88f492d3fd6f6bd35fafa0ee5b88a32facfb587d668e4574',
'/en/theses/thesis-01': '50619b636858d35c857bc38b4468b9409c58da700a0c6cb0609889f882a1e448',
'/en/theses/thesis-02': 'f9ede427b6e4ac939db8ad7584c6ea11038daee33b9cb0397b14fdfd45aa33a6',
'/en/theses/thesis-03': '29d9f0af7d2337f301e5f2d8fdde035b674cea761abea6c0c02bb8b3ff173dc0',
'/en/theses/thesis-04': '11270734f0e8218f43aa4526e6ae6a76685df7d9d040277fb0404727f58c4af2',
'/en/theses/thesis-05': 'bba1c681c3d6a8d7e3025c5d37196d2f4ea9d517146c90b33c0442f574278ba7',
'/en/theses/thesis-06': '0e60de5d2befe9346c03b6d225de6a85951c4248101c653739caf18acacdfb42',
'/en/theses/thesis-07': '4ce822008ae5bbcde4c7d07d8ea29c968b1a10fceada8595d87eea74adfc18ff',
'/en/theses/thesis-08': 'c40bdc57c7b2135ee0afd46f7eb929bf51a42bbe84d3bcca208c190d0e280714',
'/en/theses/thesis-09': 'e6f4535b9f4fcb40f9404ae2aba2cbfd5f8e568c72c2282a7e2399b7cd857681',
'/en/theses/thesis-10': '0dc6046094da40aa26292f79f552a7144024bafe1431807604d621012fb38545',
'/en/theses/thesis-11': '6fdae3fbbfcc1ae366e6bcb80c22ea4a1e205b91b1a588c88d8b462f2b9eff93',
'/en/theses/thesis-12': '3622ee15c5b6d871deded43188514fdd2bfffbce06ce4e1cf41357019e516a95',
'/en/theses/thesis-13': 'aa88c38dc737ba5dcc5038de2a7d5abecb6496fa2742c1d538f5ec1c976f3afb',
'/en/theses/thesis-14': '6cc5e720510aa64f9e89846065c2bb01fdf56925a8085f6e8cea4ec5a22e2440',
'/en/theses/thesis-15': '5fb7ec780b8dd47b401f5980aea7713c4012eed713e66495f1aed8753c7b9469',
'/en/theses/thesis-16': '1c92c3d02a630faae7dc3c004103be9756dba1d01309a72dadd06c44b132d774',
'/en/theses/thesis-17': '0fb03f09f1723e8c456d80d71a947df0e1807baf6bce7614fbfde1022d3b064d',
'/en/theses/thesis-18': '4947b4caf9d986b05575dc0e1e914674d520a00e7f2c1a6e459e2b2e63329e72',
'/en/theses/thesis-19': 'd6d2911ad8a8994914dc4a4cba9a0b420b794248c47068866bbaf64c683334e5',
'/en/theses/thesis-20': '1526fbecba340c36c16dc7e91205f9093ab7dfd25f0145370279a1e92b69e3f7',
'/en/theses/thesis-21': '65072cebb8e45bb2055ac3002e2cc016892a26ff03182360eba0bc2d23dee585',
'/en/theses/thesis-22': 'dcf3f852f0e22117cee87a078879b24530fa7019777eabdfacd8fb1abdf16f24',
'/en/theses/thesis-23': '331d6afe47b62adb9045f98a41fe14f5da5810cd196ade8cfacded7e971566d6',
'/en/theses/thesis-24': 'accff18fe13b9f251ffaba0d5bd9984f817663084ef4114a933d0dbe0a270b23',
'/en/theses/thesis-25': 'cd52b89b2e5638738bbab109999abc6014b03915bdf34b1be5869288fe21467d',
'/en/theses/thesis-26': '3001967466bb020876c68c7144513c3ccb35c221c23fe2c7f7fd9139595f8ea5',
'/en/theses/thesis-27': '1dd165ed08b54190c0ce9c15ad18a5b0e79262db457812d57d59b2fa9b52df84',
'/en/theses/thesis-28': '5cb0ce9c13c9ded042ac4d4f9528a2277baa0bceaa07eac8653aa7cea537494a',
'/en/theses/thesis-29': 'a3d66739d9129aa60933b0899d3cdf12e2fe97d26f82b8357627147e67173adc',
'/en/theses/thesis-30': 'fa06d80eda6a5c81cbf3c39cba7d9a201d33aab5d58ec9d5b85e2df5d8984dd5',
'/en/living-manifesto': '0c7fb1f1f4f5ca079db063faf05001a3321e2b6260bdb7d7c7389cf344b89d24',
    // nl/guides
  };
  return hashes[path] || null;
}