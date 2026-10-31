/* Shared behavior for every page: mobile nav + graceful photo fallbacks. */

(function () {
  'use strict';

  /* ---- Mobile navigation toggle ---------------------------------------- */
  function initNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.nav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---- Photo fallback ---------------------------------------------------
     Any <img> carrying data-fallback-initials="TK" or data-fallback-text="…"
     that fails to load (file not added yet, typo in the filename) is swapped
     for a textured maroon tile, so the layout never breaks while photos are
     still being collected.                                                 */
  function initPhotoFallbacks() {
    var imgs = document.querySelectorAll(
      'img[data-fallback-initials], img[data-fallback-text]'
    );

    Array.prototype.forEach.call(imgs, function (img) {
      function fail() {
        var holder = img.parentNode;
        if (!holder || holder.querySelector('.placeholder')) return;
        var ph = document.createElement('div');
        ph.className = 'placeholder';
        ph.setAttribute('aria-hidden', 'true');
        ph.textContent = img.getAttribute('data-fallback-initials') ||
                         img.getAttribute('data-fallback-text') || '';
        holder.appendChild(ph);
        img.remove();
      }

      img.addEventListener('error', fail);
      // Catch images that already failed before this script ran.
      if (img.complete && img.naturalWidth === 0) fail();
    });
  }

  /* ---- Tell people where a link goes ------------------------------------
     Adds a hover tooltip naming the destination for links that leave the
     site, and for mailto:/file downloads. Browsers show the raw URL in the
     status bar, but that is easy to miss and gone on touch devices.      */
  function annotateLinks() {
    var here = location.host;

    Array.prototype.forEach.call(document.querySelectorAll('a[href]'), function (a) {
      if (a.dataset.linkAnnotated) return;
      var href = a.getAttribute('href') || '';
      var note = '';

      if (/^mailto:/i.test(href)) {
        note = 'Email ' + href.replace(/^mailto:/i, '').split('?')[0];
      } else if (/^tel:/i.test(href)) {
        note = 'Call ' + href.replace(/^tel:/i, '');
      } else if (a.hasAttribute('download')) {
        note = 'Download ' + href.split('/').pop();
      } else if (/^https?:/i.test(href)) {
        var u;
        try { u = new URL(href); } catch (e) { return; }
        if (u.host !== here) {
          var where = u.host.replace(/^www\./, '') + (u.pathname === '/' ? '' : u.pathname);
          if (where.length > 60) where = where.slice(0, 57) + '…';
          note = 'Opens ' + where;
        }
      }

      if (note) {
        a.title = note;
        a.dataset.linkAnnotated = '1';
      }
    });
  }

  function start() {
    initNav();
    initPhotoFallbacks();
    annotateLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  // People page builds its cards after this file loads; let it re-run the hook.
  window.MRD = window.MRD || {};
  window.MRD.initPhotoFallbacks = initPhotoFallbacks;
  window.MRD.annotateLinks = annotateLinks;
})();
