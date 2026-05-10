// Click-to-zoom for figures: svg.fig, figure.real-fig img, figure.paper-fig img
(function(){
  if (!('querySelectorAll' in document)) return;

  function openModal(content){
    var overlay = document.createElement('div');
    overlay.className = 'fig-modal-overlay';
    var box = document.createElement('div');
    box.className = 'fig-modal-box';
    box.appendChild(content);
    var close = document.createElement('button');
    close.className = 'fig-modal-close';
    close.setAttribute('aria-label', '닫기');
    close.textContent = '×';
    box.appendChild(close);
    overlay.appendChild(box);
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';

    function destroy(){
      document.body.style.overflow = '';
      overlay.remove();
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e){
      if (e.key === 'Escape') destroy();
    }
    overlay.addEventListener('click', function(e){
      if (e.target === overlay || e.target === close) destroy();
    });
    document.addEventListener('keydown', onKey);

    // Touch: swipe down (or up) to close on mobile
    var touchStartY = null, touchStartT = 0;
    overlay.addEventListener('touchstart', function(e){
      if (e.touches.length !== 1) return;
      touchStartY = e.touches[0].clientY;
      touchStartT = Date.now();
    }, {passive:true});
    overlay.addEventListener('touchmove', function(e){
      if (touchStartY === null || e.touches.length !== 1) return;
      var dy = e.touches[0].clientY - touchStartY;
      if (Math.abs(dy) > 12) {
        // Drag follow — translate box for visual feedback
        box.style.transform = 'translateY(' + dy + 'px)';
        box.style.transition = 'none';
        overlay.style.background = 'rgba(0,0,0,' + Math.max(0.3, 0.85 - Math.abs(dy)/600) + ')';
      }
    }, {passive:true});
    overlay.addEventListener('touchend', function(e){
      if (touchStartY === null) return;
      var endY = (e.changedTouches[0] || {}).clientY || touchStartY;
      var dy = endY - touchStartY;
      var dt = Date.now() - touchStartT;
      var velocity = Math.abs(dy) / Math.max(dt, 1);
      // Close if swiped more than 100px or fast enough
      if (Math.abs(dy) > 100 || (velocity > 0.5 && Math.abs(dy) > 40)) {
        destroy();
      } else {
        box.style.transition = 'transform .2s';
        box.style.transform = '';
        overlay.style.background = '';
      }
      touchStartY = null;
    });
  }

  function bindZoom(el, makeContent){
    el.style.cursor = 'zoom-in';
    el.setAttribute('role', el.getAttribute('role') || 'button');
    el.setAttribute('tabindex', '0');
    el.addEventListener('click', function(){ openModal(makeContent()); });
    el.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openModal(makeContent());
      }
    });
  }

  function init(){
    document.querySelectorAll('svg.fig').forEach(function(svg){
      bindZoom(svg, function(){
        var clone = svg.cloneNode(true);
        clone.removeAttribute('class');
        clone.classList.add('fig-modal-svg');
        clone.removeAttribute('style');
        return clone;
      });
    });
    document.querySelectorAll('figure.real-fig img, figure.paper-fig img').forEach(function(img){
      bindZoom(img, function(){
        var big = document.createElement('img');
        big.src = img.currentSrc || img.src;
        big.alt = img.alt || '';
        big.className = 'fig-modal-img';
        return big;
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// === A11y: Skip-to-content link (auto-injected) ===
(function(){
  function inject(){
    if (document.querySelector('.skip-link')) return;
    var main = document.querySelector('main');
    if (!main) return;
    if (!main.id) main.id = 'main-content';
    var link = document.createElement('a');
    link.href = '#' + main.id;
    link.className = 'skip-link';
    link.textContent = '본문 바로가기';
    document.body.insertBefore(link, document.body.firstChild);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else { inject(); }
})();

// === Active nav state — highlight current section ===
(function(){
  function setActive(){
    var path = location.pathname;
    document.querySelectorAll('.site-nav a').forEach(function(a){
      var href = a.getAttribute('href') || '';
      if (href === '/' && path === '/') {
        a.classList.add('active');
      } else if (href !== '/' && path.indexOf(href) === 0) {
        a.classList.add('active');
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setActive);
  } else { setActive(); }
})();

// === Back to top button ===
(function(){
  function init(){
    var btn = document.createElement('button');
    btn.className = 'back-to-top';
    btn.type = 'button';
    btn.setAttribute('aria-label', '맨 위로');
    btn.innerHTML = '↑';
    btn.addEventListener('click', function(){
      window.scrollTo({top:0, behavior:'smooth'});
    });
    document.body.appendChild(btn);
    function onScroll(){
      if (window.scrollY > 600) btn.classList.add('visible');
      else btn.classList.remove('visible');
    }
    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();

// === Auto abbr[title] for common hepatology abbreviations (first occurrence per page) ===
// Runs only inside <main> content, skips headings, anchors, and pre/code.
(function(){
  var DICT = {
    'HCC':   'Hepatocellular Carcinoma — 간세포암',
    'HBV':   'Hepatitis B Virus — B형간염 바이러스',
    'HCV':   'Hepatitis C Virus — C형간염 바이러스',
    'HBsAg': 'Hepatitis B surface Antigen — B형간염 표면항원',
    'HBeAg': 'Hepatitis B e Antigen — B형간염 e항원',
    'AFP':   'Alpha-Fetoprotein — 종양표지자',
    'ALT':   'Alanine Aminotransferase — 간세포 손상 지표',
    'AST':   'Aspartate Aminotransferase — 간세포 손상 지표',
    'ALP':   'Alkaline Phosphatase — 담도 효소',
    'GGT':   'Gamma-Glutamyl Transferase — 담도 효소',
    'BCLC':  'Barcelona Clinic Liver Cancer — HCC 병기 분류',
    'MELD':  'Model for End-stage Liver Disease — 간기능 점수',
    'MASLD': 'Metabolic dysfunction-Associated Steatotic Liver Disease — 대사이상지방간질환',
    'MASH':  'Metabolic dysfunction-Associated Steatohepatitis — 대사이상지방간염',
    'NAFLD': 'Non-Alcoholic Fatty Liver Disease — 비알코올성 지방간 (구 명칭, MASLD로 대체)',
    'NASH':  'Non-Alcoholic Steatohepatitis — 비알코올성 지방간염 (구 명칭)',
    'TACE':  'Transarterial Chemoembolization — 경동맥 화학색전술',
    'TARE':  'Transarterial Radioembolization — 경동맥 방사선색전술',
    'RFA':   'Radiofrequency Ablation — 고주파 소작술',
    'MWA':   'Microwave Ablation — 마이크로파 소작술',
    'SBRT':  'Stereotactic Body Radiation Therapy — 정위방사선치료',
    'TIPS':  'Transjugular Intrahepatic Portosystemic Shunt — 경경정맥 간내 문맥대정맥 단락술',
    'DAA':   'Direct-Acting Antiviral — C형간염 직접작용 항바이러스제',
    'TDF':   'Tenofovir Disoproxil Fumarate — 테노포비어 DF',
    'TAF':   'Tenofovir Alafenamide — 테노포비어 AF',
    'ETV':   'Entecavir — 엔테카비어',
    'AIH':   'Autoimmune Hepatitis — 자가면역간염',
    'PBC':   'Primary Biliary Cholangitis — 원발담즙성 담관염',
    'PSC':   'Primary Sclerosing Cholangitis — 원발경화성 담관염',
    'CTP':   'Child-Turcotte-Pugh — 간경변 점수',
    'INR':   'International Normalized Ratio — 응고 시간 지표',
    'PT':    'Prothrombin Time — 응고 시간',
    'CT':    'Computed Tomography — 전산화단층촬영',
    'MRI':   'Magnetic Resonance Imaging — 자기공명영상',
    'PMC':   'PubMed Central — 미국 NIH 무료 의학논문 저장소',
    'OS':    'Overall Survival — 전체 생존',
    'PFS':   'Progression-Free Survival — 무진행 생존',
    'ORR':   'Objective Response Rate — 객관적 반응률',
    'HR':    'Hazard Ratio — 위험비',
    'OR':    'Odds Ratio — 교차비',
    'RCT':   'Randomized Controlled Trial — 무작위 대조 임상시험',
    'GLP-1': 'Glucagon-Like Peptide-1',
    'SGLT2': 'Sodium-Glucose Cotransporter 2',
    'PIVKA-II': 'Protein Induced by Vitamin K Absence-II — DCP, HCC 표지자',
    'STRIDE': 'Single Tremelimumab Regular Interval Durvalumab — HIMALAYA 트라이얼 요법',
    'CIK':   'Cytokine-Induced Killer cell — 사이토카인 유도 살해세포'
  };

  function init(){
    var main = document.querySelector('main');
    if (!main) return;
    // Build sorted key list — longer terms first to avoid partial matches (HBsAg before HBV, GLP-1 before GLP)
    var keys = Object.keys(DICT).sort(function(a,b){ return b.length - a.length; });
    var seen = {}; // first-occurrence-only

    // Walk text nodes, but skip inside these tags
    var SKIP = {SCRIPT:1,STYLE:1,A:1,ABBR:1,CODE:1,PRE:1,H1:1,H2:1,H3:1,H4:1,H5:1,H6:1,BUTTON:1,SVG:1};
    function walk(node){
      if (node.nodeType === 1) {
        if (SKIP[node.tagName]) return;
        // Don't descend into elements that already are abbr or links
        var children = Array.prototype.slice.call(node.childNodes);
        children.forEach(walk);
        return;
      }
      if (node.nodeType !== 3) return;
      var text = node.nodeValue;
      if (!text || text.length < 2) return;

      // Find earliest unseen abbreviation
      for (var i = 0; i < keys.length; i++) {
        var k = keys[i];
        if (seen[k]) continue;
        // Word boundary: surround with non-alnum (or start/end)
        // Use literal match because some keys contain '-'
        var idx = text.indexOf(k);
        while (idx !== -1) {
          var before = idx === 0 ? '' : text.charAt(idx-1);
          var after = (idx + k.length >= text.length) ? '' : text.charAt(idx + k.length);
          var beforeOK = !before || !/[A-Za-z0-9가-힣]/.test(before);
          var afterOK = !after || !/[A-Za-z0-9가-힣]/.test(after);
          if (beforeOK && afterOK) break;
          idx = text.indexOf(k, idx + 1);
        }
        if (idx === -1) continue;

        // Split text node and wrap match in <abbr>
        var parent = node.parentNode;
        if (!parent) return;
        var pre = text.substring(0, idx);
        var match = text.substring(idx, idx + k.length);
        var post = text.substring(idx + k.length);
        var abbr = document.createElement('abbr');
        abbr.title = DICT[k];
        abbr.textContent = match;
        var frag = document.createDocumentFragment();
        if (pre) frag.appendChild(document.createTextNode(pre));
        frag.appendChild(abbr);
        var postNode = null;
        if (post) {
          postNode = document.createTextNode(post);
          frag.appendChild(postNode);
        }
        parent.replaceChild(frag, node);
        seen[k] = true;
        // Continue scanning the post portion for OTHER abbreviations
        if (postNode) walk(postNode);
        return;
      }
    }
    walk(main);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();

// Rewrite SNUH links to mobile variant on small screens.
// Desktop: https://www.snuh.org/blog/...    Mobile: https://www.snuh.org/m/blog/...
(function(){
  function rewriteSnuh(){
    var isMobile = window.matchMedia('(max-width: 768px)').matches;
    document.querySelectorAll('a[href*="snuh.org"]').forEach(function(a){
      var href = a.getAttribute('href');
      if (!href) return;
      var hasMobile = href.indexOf('snuh.org/m/') >= 0;
      if (isMobile && !hasMobile) {
        a.setAttribute('href', href.replace('snuh.org/blog/', 'snuh.org/m/blog/'));
      } else if (!isMobile && hasMobile) {
        a.setAttribute('href', href.replace('snuh.org/m/blog/', 'snuh.org/blog/'));
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', rewriteSnuh);
  } else {
    rewriteSnuh();
  }
})();
