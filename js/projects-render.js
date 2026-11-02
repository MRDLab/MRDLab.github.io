/* Builds a projects page from the projects/ folder.

   projects/index.json           every project slug and its status
   projects/<slug>/project.json  that project's text and media list
   projects/<slug>/<file>        the images and videos themselves

   The page decides what it shows via a mount element:

     <div id="projects-list" data-status="active"></div>   current work
     <div id="projects-list" data-status="past"></div>     completed work

   To change a project, edit its project.json. To add one, make a folder,
   add a project.json, and list the slug in index.json. Nothing here needs
   to change. */

(function () {
  'use strict';

  var ROOT = 'projects/';
  // Always revalidate with the server so an edit shows up immediately
  // instead of waiting out the CDN cache.
  var FRESH = { cache: 'no-cache' };

  var mount = document.getElementById('projects-list');
  if (!mount) return;
  var WANT = mount.getAttribute('data-status') || 'past';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  /* ---- Media ------------------------------------------------------------ */

  function mediaNode(item, dir) {
    var fig = el('figure', 'media-item');

    if (item.type === 'youtube') {
      var frameWrap = el('div', 'media-embed');
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + item.id;
      iframe.title = item.title || 'Project video';
      iframe.loading = 'lazy';
      iframe.allow = 'accelerometer; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      frameWrap.appendChild(iframe);
      fig.appendChild(frameWrap);

    } else if (item.type === 'video') {
      // Converted from the original site's animated GIFs — autoplay muted so
      // they behave the way the GIFs did, but at a fraction of the weight.
      var video = document.createElement('video');
      video.src = dir + item.file;
      if (item.poster) video.poster = dir + item.poster;
      video.autoplay = true;
      video.loop = true;
      video.muted = true;
      video.playsInline = true;
      video.setAttribute('muted', '');
      video.setAttribute('playsinline', '');
      video.controls = true;
      video.preload = 'metadata';
      if (item.alt) video.setAttribute('aria-label', item.alt);
      fig.appendChild(video);

    } else {
      var img = document.createElement('img');
      img.src = dir + item.file;
      img.alt = item.alt || '';
      img.loading = 'lazy';
      fig.appendChild(img);
    }

    if (item.caption) fig.appendChild(el('figcaption', null, item.caption));
    return fig;
  }

  /* ---- One project ------------------------------------------------------ */

  function projectNode(slug, status, data) {
    var dir = ROOT + slug + '/';
    var article = el('article', 'project-entry');
    article.id = slug;

    var head = el('div', 'project-head');
    if (data.tagline) head.appendChild(el('p', 'tagline', data.tagline));

    var h3 = el('h3', null, data.title);
    head.appendChild(h3);

    if (status === 'past') {
      var badge = el('span', 'badge badge-past', 'Completed');
      h3.appendChild(document.createTextNode(' '));
      h3.appendChild(badge);
    }
    article.appendChild(head);

    var grid = el('div', 'project-grid');

    // Media column
    var mediaCol = el('div', 'project-media-col');
    (data.media || []).forEach(function (m) { mediaCol.appendChild(mediaNode(m, dir)); });
    if (!(data.media || []).length) {
      mediaCol.appendChild(el('div', 'media-placeholder', 'Add media to ' + dir));
    }

    // Text column
    var textCol = el('div', 'project-text-col');
    (data.body || []).forEach(function (p) { textCol.appendChild(el('p', null, p)); });

    // Prominent calls to action — a live demo, a partner announcement.
    // Rendered as buttons, above the credit line.
    if ((data.links || []).length) {
      var linkRow = el('p', 'project-links');
      data.links.forEach(function (l, i) {
        var a = el('a', 'btn ' + (i === 0 ? 'btn-maroon' : 'btn-outline'), l.label);
        a.href = l.url;
        a.target = '_blank';
        a.rel = 'noopener';
        linkRow.appendChild(a);
      });
      textCol.appendChild(linkRow);
    }

    if (data.researchers) {
      var r = el('p', 'researchers');
      r.appendChild(el('strong', null, 'Researchers: '));
      r.appendChild(document.createTextNode(data.researchers));
      textCol.appendChild(r);
    }

    if ((data.publications || []).length) {
      var details = el('details', 'pubs');
      // Most projects list the lab's own papers; a project can override the
      // wording (e.g. "Relevant publications") via publicationsLabel.
      details.appendChild(el('summary', null,
        (data.publicationsLabel || 'Publications') +
        ' (' + data.publications.length + ')'));
      var ul = el('ul');
      data.publications.forEach(function (p) {
        var li = document.createElement('li');
        if (p.url) {
          var a = el('a', null, p.label);
          a.href = p.url;
          a.target = '_blank';
          a.rel = 'noopener';
          li.appendChild(a);
        } else {
          li.appendChild(document.createTextNode(p.label));
        }
        ul.appendChild(li);
      });
      details.appendChild(ul);
      textCol.appendChild(details);
    }

    grid.appendChild(mediaCol);
    grid.appendChild(textCol);
    article.appendChild(grid);
    return article;
  }

  /* ---- Page ------------------------------------------------------------- */

  function showEmptyState() {
    // The page supplies its own wording; fall back to something sensible.
    var tpl = document.getElementById('projects-empty');
    if (tpl) {
      tpl.hidden = false;
    } else {
      mount.appendChild(el('p', null, 'Nothing to show here yet.'));
    }
  }

  fetch(ROOT + 'index.json', FRESH)
    .then(function (r) {
      if (!r.ok) throw new Error('index.json: HTTP ' + r.status);
      return r.json();
    })
    .then(function (index) {
      var wanted = (index.projects || []).filter(function (e) {
        return WANT === 'active' ? e.status === 'active' : e.status !== 'active';
      });

      return Promise.all(wanted.map(function (entry) {
        return fetch(ROOT + entry.slug + '/project.json', FRESH)
          .then(function (r) {
            if (!r.ok) throw new Error(entry.slug + ': HTTP ' + r.status);
            return r.json();
          })
          .then(function (data) {
            return { slug: entry.slug, status: entry.status, data: data };
          })
          .catch(function (err) {
            console.error('Could not load project', entry.slug, err);
            return null;
          });
      }));
    })
    .then(function (all) {
      var ok = all.filter(Boolean);
      if (!ok.length) { showEmptyState(); return; }
      ok.forEach(function (e) {
        mount.appendChild(projectNode(e.slug, e.status, e.data));
      });
      if (window.MRD && window.MRD.annotateLinks) window.MRD.annotateLinks();
    })
    .catch(function (err) {
      console.error(err);
      mount.appendChild(el('p', null,
        'Projects could not be loaded. If you are opening this file directly, ' +
        'run a local server instead: python3 -m http.server 8000'));
    });
})();
