/* =========================================================================
   GTS RISK ADVISORY  ·  OPERATIONAL FOOTPRINT
   Renders the operating-country list and the Africa silhouette map on the
   /about/ page from /data/footprint.json. Reuses the shared SVG loader in
   assets/js/africa-map.js so the africa.svg fetch is shared with the heat
   map (memoised per page load).
   ========================================================================= */

(function () {
  'use strict';

  const ENDPOINT = '/data/footprint.json';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const supportsHover = window.matchMedia('(hover: hover)').matches;

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /** Sort alphabetically, but pin HQ to the top. */
  function sortCountries(list) {
    return [...list].sort((a, b) => {
      if (a.hq && !b.hq) return -1;
      if (b.hq && !a.hq) return 1;
      return a.name.localeCompare(b.name);
    });
  }

  function renderList(listEl, countries) {
    listEl.innerHTML = sortCountries(countries).map((c) => {
      const hq = c.hq ? ' <span class="footprint-list__hq" aria-label="Headquarters">HQ</span>' : '';
      return `<li data-country-iso="${escapeHtml(c.iso)}">${escapeHtml(c.name)}${hq}</li>`;
    }).join('');
  }

  async function renderMap(container, countries) {
    if (!window.GTSAfricaMap || !window.GTSAfricaMap.loadSvgMarkup) {
      console.error('GTSAfricaMap loader missing — load africa-map.js before footprint.js.');
      return;
    }
    const operatingSet = new Set(countries.map((c) => c.iso));
    const byIso = {};
    countries.forEach((c) => { byIso[c.iso] = c; });

    const markup = await window.GTSAfricaMap.loadSvgMarkup();
    container.innerHTML = markup;
    const svg = container.querySelector('svg');
    if (!svg) return;

    svg.removeAttribute('width');
    svg.removeAttribute('height');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');

    svg.querySelectorAll('path.country').forEach((p) => {
      const iso = p.getAttribute('data-iso');
      if (operatingSet.has(iso)) {
        const c = byIso[iso];
        p.classList.add('is-operating');
        p.setAttribute('data-operating', 'true');
        p.setAttribute('aria-label', `GTS operating market: ${c.name}`);
      } else {
        p.classList.add('is-non-operating');
        p.setAttribute('aria-hidden', 'true');
      }
    });

    // Headquarters marker — placed at the centroid of the HQ country path.
    const hq = countries.find((c) => c.hq);
    if (hq) {
      const hqPath = svg.querySelector(`path.country[data-iso="${hq.iso}"]`);
      if (hqPath) {
        const bbox = hqPath.getBBox();
        const cx = bbox.x + bbox.width / 2;
        const cy = bbox.y + bbox.height / 2;
        const ns = 'http://www.w3.org/2000/svg';

        const group = document.createElementNS(ns, 'g');
        group.setAttribute('class', 'footprint-hq');
        group.setAttribute('aria-label', `Headquarters: ${hq.name}`);

        // Pulsing ring (rendered behind the dot)
        const ring = document.createElementNS(ns, 'circle');
        ring.setAttribute('class', 'footprint-hq__pulse');
        ring.setAttribute('cx', cx);
        ring.setAttribute('cy', cy);
        ring.setAttribute('r', '6');
        group.appendChild(ring);

        // Solid HQ dot
        const dot = document.createElementNS(ns, 'circle');
        dot.setAttribute('class', 'footprint-hq__dot');
        dot.setAttribute('cx', cx);
        dot.setAttribute('cy', cy);
        dot.setAttribute('r', '6');
        group.appendChild(dot);

        svg.appendChild(group);
      }
    }

    return svg;
  }

  function bindHoverSync(listEl, mapEl) {
    if (!supportsHover) return; // touch devices: skip the cross-highlight

    const setHover = (iso, on) => {
      if (!iso) return;
      const path = mapEl.querySelector(`path.country[data-iso="${iso}"]`);
      const item = listEl.querySelector(`li[data-country-iso="${iso}"]`);
      if (path && path.classList.contains('is-operating')) {
        path.classList.toggle('is-hover', on);
      }
      if (item) item.classList.toggle('is-hover', on);
    };

    listEl.addEventListener('mouseover', (e) => {
      const li = e.target.closest('li[data-country-iso]');
      if (li) setHover(li.getAttribute('data-country-iso'), true);
    });
    listEl.addEventListener('mouseout', (e) => {
      const li = e.target.closest('li[data-country-iso]');
      if (li) setHover(li.getAttribute('data-country-iso'), false);
    });

    mapEl.addEventListener('mouseover', (e) => {
      const path = e.target.closest('path.country.is-operating');
      if (path) setHover(path.getAttribute('data-iso'), true);
    });
    mapEl.addEventListener('mouseout', (e) => {
      const path = e.target.closest('path.country.is-operating');
      if (path) setHover(path.getAttribute('data-iso'), false);
    });
  }

  document.addEventListener('DOMContentLoaded', async () => {
    const mapEl = document.getElementById('footprint-map');
    const listEl = document.getElementById('footprint-list');
    if (!mapEl && !listEl) return;

    try {
      const res = await fetch(ENDPOINT);
      if (!res.ok) throw new Error('footprint.json ' + res.status);
      const data = await res.json();
      const countries = data.operating_countries || [];

      if (listEl) renderList(listEl, countries);
      if (mapEl) {
        await renderMap(mapEl, countries);
        if (prefersReducedMotion) mapEl.classList.add('reduced-motion');
      }
      if (listEl && mapEl) bindHoverSync(listEl, mapEl);

      // ISO-coverage report (dev aid — runs once per page load).
      if (mapEl) {
        const present = new Set(
          Array.from(mapEl.querySelectorAll('path.country')).map((p) => p.getAttribute('data-iso'))
        );
        const missing = countries.filter((c) => !present.has(c.iso));
        if (missing.length) {
          console.warn('Footprint: ISO codes not present in africa.svg:', missing.map((c) => c.iso));
        }
      }
    } catch (err) {
      console.error('Operational footprint failed to load:', err);
    }
  });
})();
