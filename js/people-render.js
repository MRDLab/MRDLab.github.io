/* Builds the People page from js/people-data.js. No editing needed here —
   change the roster in people-data.js instead. */

(function () {
  'use strict';

  var data = (window.MRD && window.MRD.people) || null;
  if (!data) return;

  var PHOTO_DIR = 'images/people/';

  // Degree and generational suffixes are not part of the name.
  var SUFFIXES = /^(phd|md|ms|msme|bs|bsme|dsc|scd|jr|sr|ii|iii|iv)$/i;

  function initials(name) {
    var parts = String(name)
      .split(/[\s,]+/)
      .map(function (p) { return p.replace(/[^A-Za-z'-]/g, ''); })
      .filter(function (p) { return p && !SUFFIXES.test(p); });

    if (!parts.length) return '?';
    var first = parts[0].charAt(0);
    var last = parts.length > 1 ? parts[parts.length - 1].charAt(0) : '';
    return (first + last).toUpperCase();
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  /* Photo holder: real <img> when a filename is given, maroon initials tile
     otherwise. site.js swaps a broken <img> for the tile automatically. */
  function photoNode(person) {
    var holder = el('div', 'photo');

    if (person.photo) {
      var img = document.createElement('img');
      img.src = PHOTO_DIR + person.photo;
      img.alt = person.name;
      img.loading = 'lazy';
      img.setAttribute('data-fallback-initials', initials(person.name));
      holder.appendChild(img);
    } else {
      var ph = el('div', 'placeholder', initials(person.name));
      ph.setAttribute('aria-hidden', 'true');
      holder.appendChild(ph);
    }
    return holder;
  }

  function linksNode(person) {
    var list = [];
    if (person.email) list.push({ label: 'Email', url: 'mailto:' + person.email });
    if (person.links) {
      person.links.forEach(function (l) {
        // Don't repeat an email link that's already covered above.
        if (person.email && l.url === 'mailto:' + person.email) return;
        list.push(l);
      });
    }
    if (!list.length) return null;

    var wrap = el('p', 'links');
    list.forEach(function (l) {
      var a = el('a', null, l.label);
      a.href = l.url;
      if (!/^mailto:/.test(l.url)) {
        a.target = '_blank';
        a.rel = 'noopener';
      }
      wrap.appendChild(a);
    });
    return wrap;
  }

  function personCard(person, lead) {
    var card = el('article', lead ? 'person person-lead' : 'person');
    card.appendChild(photoNode(person));

    var info = el('div', 'info');
    info.appendChild(el('h3', 'name', person.name));
    info.appendChild(el('p', 'role', person.role || ''));
    if (person.blurb) info.appendChild(el('p', 'blurb', person.blurb));

    var links = linksNode(person);
    if (links) info.appendChild(links);

    card.appendChild(info);
    return card;
  }

  /* ---- Lead faculty ---------------------------------------------------- */
  var leadMount = document.getElementById('lead-faculty');
  if (leadMount && data.lead) {
    leadMount.appendChild(personCard(data.lead, true));
  }

  /* ---- Groups ----------------------------------------------------------- */
  var groupMount = document.getElementById('people-groups');
  if (groupMount && data.groups) {
    data.groups.forEach(function (group) {
      if (!group.members || !group.members.length) return;

      var head = el('div', 'section-head');
      head.appendChild(el('h2', null, group.title));
      groupMount.appendChild(head);

      var grid = el('div', 'people-grid');
      group.members.forEach(function (m) { grid.appendChild(personCard(m, false)); });
      groupMount.appendChild(grid);

      // Breathing room before the next group heading.
      grid.style.marginBottom = '48px';
    });
  }

  /* ---- Alumni ----------------------------------------------------------- */
  var alumniMount = document.getElementById('alumni-list');
  if (alumniMount && data.alumni) {
    data.alumni.forEach(function (a) {
      var li = document.createElement('li');
      li.appendChild(document.createTextNode(a.name));
      if (a.degree) li.appendChild(el('span', 'yr', a.degree));
      alumniMount.appendChild(li);
    });
  }

  // Re-arm fallbacks for the <img> elements we just created.
  if (window.MRD.initPhotoFallbacks) window.MRD.initPhotoFallbacks();
})();
