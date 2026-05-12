/* drshin.kr 사이트 내 검색 — vanilla JS, 의존성 없음 */
(function () {
  'use strict';

  var CAT_LABEL = {
    hub: '대주제',
    detail: '세부주제',
    case: '사례',
    cc: '증상별',
    update: '최신지견',
    page: '페이지',
    home: '홈',
  };
  var CAT_CLS = {
    hub: 'cat-hub',
    detail: 'cat-detail',
    case: 'cat-case',
    cc: 'cat-cc',
    update: 'cat-update',
    page: 'cat-page',
    home: 'cat-home',
  };

  var index = null;
  var loading = null;
  var input, results, root, hits, status;
  var activeIdx = -1;
  var lastQuery = '';

  function debounce(fn, ms) {
    var t;
    return function () {
      var a = arguments, c = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(c, a); }, ms);
    };
  }

  function ensureIndex() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = fetch('/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; return index; })
      .catch(function () { index = []; return index; });
    return loading;
  }

  function tokenize(s) {
    return s.toLowerCase().split(/[\s,·.\/\-_·:;!?"'`()\[\]{}]+/).filter(function (t) { return t.length > 0; });
  }

  function scoreEntry(e, queryTokens, queryRaw) {
    if (!queryTokens.length) return 0;
    var t = (e.t || '').toLowerCase();
    var tl = (e.tl || '').toLowerCase();
    var d = (e.d || '').toLowerCase();
    var k = (e.k || '').toLowerCase();
    var score = 0;
    var titleMatches = 0;
    for (var i = 0; i < queryTokens.length; i++) {
      var q = queryTokens[i];
      if (t.indexOf(q) !== -1) { score += 50; titleMatches++; }
      if (tl.indexOf(q) !== -1) score += 30;
      if (d.indexOf(q) !== -1) score += 12;
      if (k.indexOf(q) !== -1) score += 18;
    }
    // 모든 token이 title에 매칭되면 추가 보너스
    if (titleMatches === queryTokens.length) score += 30;
    // 정확한 phrase 매칭
    var phrase = queryRaw.toLowerCase().trim();
    if (phrase.length >= 2) {
      if (t.indexOf(phrase) !== -1) score += 40;
      if (tl.indexOf(phrase) !== -1) score += 25;
    }
    return score;
  }

  function highlight(text, tokens) {
    if (!text) return '';
    var escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    if (!tokens.length) return escaped;
    var pattern = tokens.map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|');
    if (!pattern) return escaped;
    return escaped.replace(new RegExp('(' + pattern + ')', 'gi'), '<mark>$1</mark>');
  }

  function render(query) {
    var tokens = tokenize(query);
    if (!index || !tokens.length) {
      results.innerHTML = '';
      hits.textContent = '';
      root.classList.remove('has-results');
      return;
    }
    var ranked = [];
    for (var i = 0; i < index.length; i++) {
      var sc = scoreEntry(index[i], tokens, query);
      if (sc > 0) ranked.push({ s: sc, e: index[i] });
    }
    ranked.sort(function (a, b) { return b.s - a.s; });
    var top = ranked.slice(0, 12);
    var html = '';
    for (var j = 0; j < top.length; j++) {
      var e = top[j].e;
      var cat = CAT_LABEL[e.c] || e.c;
      var catCls = CAT_CLS[e.c] || '';
      var title = highlight(e.t, tokens);
      var desc = e.d ? highlight(e.d, tokens) : '';
      html += '<li role="option" data-href="' + e.u + '">'
        + '<a href="' + e.u + '">'
        + '<span class="search-cat ' + catCls + '">' + cat + '</span>'
        + '<span class="search-body">'
        + '<span class="search-title">' + title + '</span>'
        + (desc ? '<span class="search-desc">' + desc + '</span>' : '')
        + '</span></a></li>';
    }
    results.innerHTML = html;
    hits.textContent = ranked.length ? (ranked.length + '개 결과') : '결과 없음';
    root.classList.add('has-results');
    activeIdx = -1;
  }

  function setActive(idx) {
    var items = results.querySelectorAll('li');
    if (!items.length) return;
    if (idx < 0) idx = items.length - 1;
    if (idx >= items.length) idx = 0;
    items.forEach(function (li, i) {
      if (i === idx) li.classList.add('active');
      else li.classList.remove('active');
    });
    activeIdx = idx;
    items[idx].scrollIntoView({ block: 'nearest' });
  }

  function open() { root.classList.add('open'); document.body.classList.add('search-open'); }
  function close() {
    root.classList.remove('open');
    root.classList.remove('has-results');
    document.body.classList.remove('search-open');
    input.value = '';
    results.innerHTML = '';
    hits.textContent = '';
    activeIdx = -1;
  }

  function init() {
    root = document.getElementById('site-search');
    if (!root) return;
    input = root.querySelector('.search-input');
    results = root.querySelector('.search-results');
    hits = root.querySelector('.search-hits');
    status = root.querySelector('.search-status');

    var onInput = debounce(function () {
      var q = input.value.trim();
      if (q === lastQuery) return;
      lastQuery = q;
      if (!q) {
        results.innerHTML = '';
        hits.textContent = '';
        root.classList.remove('has-results');
        return;
      }
      render(q);
    }, 60);

    input.addEventListener('focus', function () {
      open();
      ensureIndex();
    });
    input.addEventListener('input', function () {
      ensureIndex().then(function () { onInput(); });
    });
    input.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { close(); input.blur(); }
      else if (ev.key === 'ArrowDown') { ev.preventDefault(); setActive(activeIdx + 1); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); setActive(activeIdx - 1); }
      else if (ev.key === 'Enter') {
        var items = results.querySelectorAll('li');
        if (activeIdx >= 0 && items[activeIdx]) {
          ev.preventDefault();
          window.location.href = items[activeIdx].dataset.href;
        }
      }
    });

    // Click outside closes
    document.addEventListener('click', function (ev) {
      if (root.contains(ev.target)) return;
      if (root.classList.contains('open')) close();
    });

    // Global keyboard shortcut: '/' or Ctrl/Cmd+K to focus
    document.addEventListener('keydown', function (ev) {
      if (ev.key === '/' && document.activeElement !== input
          && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) {
        ev.preventDefault();
        input.focus();
      } else if ((ev.metaKey || ev.ctrlKey) && ev.key === 'k') {
        ev.preventDefault();
        input.focus();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
