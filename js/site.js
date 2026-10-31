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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initNav();
      initPhotoFallbacks();
    });
  } else {
    initNav();
    initPhotoFallbacks();
  }

  // People page builds its cards after this file loads; let it re-run the hook.
  window.MRD = window.MRD || {};
  window.MRD.initPhotoFallbacks = initPhotoFallbacks;
})();
