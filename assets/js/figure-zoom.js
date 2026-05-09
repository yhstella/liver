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
