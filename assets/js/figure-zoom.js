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
