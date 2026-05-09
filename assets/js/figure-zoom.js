// Click-to-zoom for SVG figures (svg.fig)
(function(){
  if (!('querySelectorAll' in document)) return;

  function openModal(svg, caption){
    var overlay = document.createElement('div');
    overlay.className = 'fig-modal-overlay';
    var box = document.createElement('div');
    box.className = 'fig-modal-box';
    var clone = svg.cloneNode(true);
    clone.removeAttribute('class');
    clone.classList.add('fig-modal-svg');
    clone.removeAttribute('style');
    box.appendChild(clone);
    if (caption) {
      var cap = document.createElement('p');
      cap.className = 'fig-modal-caption';
      cap.textContent = caption;
      box.appendChild(cap);
    }
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

  function init(){
    var figs = document.querySelectorAll('svg.fig');
    figs.forEach(function(svg){
      svg.style.cursor = 'zoom-in';
      svg.setAttribute('role', svg.getAttribute('role') || 'button');
      svg.setAttribute('tabindex', '0');
      var caption = '';
      var next = svg.nextElementSibling;
      if (next && next.classList && next.classList.contains('fig-caption')) {
        caption = next.textContent || '';
      }
      svg.addEventListener('click', function(){ openModal(svg, caption); });
      svg.addEventListener('keydown', function(e){
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openModal(svg, caption); }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
