/*
 * Navigation verticale pour le HTML Marp (bespoke).
 * Injecté dans 3-presentation/tolkien.html par scripts/inject-nav.mjs.
 *
 * Une slide marquée `<!-- _class: annexe ... -->` est une slide verticale :
 * elle se rattache à la slide principale (non annexe) qui la précède.
 *
 *   → / PageDown / Espace      slide principale suivante (saute les annexes)
 *   ← / PageUp / Maj+Espace    slide principale précédente
 *   ↓                          annexe suivante de la slide courante
 *   ↑                          remonte d'une annexe (jusqu'à la principale)
 *   Maj + flèche               navigation linéaire d'origine (toutes les slides)
 */
(function () {
  if (window.self !== window.top) return; // pas dans l'aperçu « slide suivante »

  function slides() {
    return Array.prototype.slice.call(document.querySelectorAll('svg.bespoke-marp-slide'));
  }
  function isAnnexe(svg) {
    var s = svg && svg.querySelector('section');
    return !!(s && s.classList.contains('annexe'));
  }
  function current(list) {
    for (var i = 0; i < list.length; i++) {
      if (list[i].classList.contains('bespoke-marp-active')) return i;
    }
    return -1;
  }
  function hasHiddenFragment(svg) {
    return !!svg.querySelector('[data-bespoke-marp-fragment=inactive]');
  }
  function go(i) {
    location.hash = '#' + (i + 1);
  }

  // Repères visuels : ▾ s'il y a une annexe dessous, ▴ sur les annexes.
  function addMarkers() {
    var style = document.createElement('style');
    style.textContent =
      'section .nav-v{position:absolute;left:0.9em;bottom:0.5em;font-size:0.6em;' +
      'line-height:1;opacity:.45;pointer-events:none;color:inherit;letter-spacing:.2em}';
    document.head.appendChild(style);
    var list = slides();
    list.forEach(function (svg, i) {
      var up = isAnnexe(svg);
      var down = i + 1 < list.length && isAnnexe(list[i + 1]);
      if (!up && !down) return;
      var m = document.createElement('div');
      m.className = 'nav-v';
      m.textContent = (up ? '▴' : '') + (down ? '▾' : '');
      svg.querySelector('section').appendChild(m);
    });
  }

  window.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey && e.key !== ' ') return;
    var view = document.body.getAttribute('data-bespoke-view');
    if (view === 'overview') return;
    var t = e.target;
    if (t && (/^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(t.nodeName) || t.isContentEditable)) return;

    var list = slides();
    var i = current(list);
    if (i < 0) return;
    var k = e.key;
    var target = null;

    if (k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) {
      if (hasHiddenFragment(list[i])) return; // laisser Marp révéler les fragments
      for (var j = i + 1; j < list.length; j++) if (!isAnnexe(list[j])) { target = j; break; }
      if (target === null) target = i;
    } else if (k === 'ArrowLeft' || k === 'PageUp' || (k === ' ' && e.shiftKey)) {
      var p = i;
      while (p > 0 && isAnnexe(list[p])) p--; // slide principale de la pile courante
      target = p;
      for (var q = p - 1; q >= 0; q--) if (!isAnnexe(list[q])) { target = q; break; }
    } else if (k === 'ArrowDown') {
      target = i + 1 < list.length && isAnnexe(list[i + 1]) ? i + 1 : i;
    } else if (k === 'ArrowUp') {
      target = isAnnexe(list[i]) ? i - 1 : i;
    } else {
      return;
    }

    e.preventDefault();
    e.stopImmediatePropagation();
    if (target !== i) go(target);
  }, true);

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addMarkers);
  else addMarkers();
})();
