/* =========================================================================
   GTS RISK ADVISORY  ·  AFRICA MAP LOADER
   Shared helpers for both the home-page teaser and the main heat-map page.
   Exposes window.GTSAfricaMap and bootstraps the static home teaser
   (#home-africa-map) lazily via IntersectionObserver.
   ========================================================================= */

(function () {
  'use strict';

  const MAP_URL = '/assets/img/maps/africa.svg';
  const DATA_URL = '/data/heat-map.json';

  let svgPromise = null;
  let dataPromise = null;

  function loadSvgMarkup() {
    if (!svgPromise) {
      svgPromise = fetch(MAP_URL).then((r) => {
        if (!r.ok) throw new Error('africa.svg ' + r.status);
        return r.text();
      });
    }
    return svgPromise;
  }

  function loadHeatMapData() {
    if (!dataPromise) {
      dataPromise = fetch(DATA_URL).then((r) => {
        if (!r.ok) throw new Error('heat-map.json ' + r.status);
        return r.json();
      });
    }
    return dataPromise;
  }

  function riskColor(r) {
    return ({
      low:      'var(--risk-low)',
      moderate: 'var(--risk-moderate)',
      elevated: 'var(--risk-elevated)',
      high:     'var(--risk-high)',
      extreme:  'var(--risk-extreme)',
    })[r] || 'var(--risk-na)';
  }

  /**
   * Inject the Africa SVG into `container` and apply per-country fills
   * from the supplied iso3 -> country record map.
   * Returns the injected <svg> element (or null on failure).
   */
  async function injectMap(container, countriesByIso3) {
    const markup = await loadSvgMarkup();
    container.innerHTML = markup;
    const svg = container.querySelector('svg');
    if (!svg) return null;

    // Make the SVG fluid.
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');

    svg.querySelectorAll('path.country').forEach((p) => {
      const iso = p.getAttribute('data-iso');
      const c = iso ? countriesByIso3[iso] : null;
      if (c) {
        p.setAttribute('fill', riskColor(c.risk));
        p.setAttribute('data-region', c.region || '');
      } else {
        p.setAttribute('fill', 'var(--risk-na)');
      }
    });

    return svg;
  }

  window.GTSAfricaMap = {
    loadSvgMarkup,
    loadHeatMapData,
    injectMap,
    riskColor,
  };

  /* ----- Home-page teaser bootstrap (lazy) ------------------------------ */
  document.addEventListener('DOMContentLoaded', () => {
    const teaser = document.getElementById('home-africa-map');
    if (!teaser) return;

    const start = () => initTeaser(teaser);

    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            obs.disconnect();
            start();
          }
        });
      }, { rootMargin: '200px' });
      obs.observe(teaser);
    } else {
      start();
    }
  });

  async function initTeaser(container) {
    try {
      const data = await loadHeatMapData();
      const byIso = {};
      data.countries.forEach((c) => { byIso[c.iso] = c; });

      const svg = await injectMap(container, byIso);
      if (!svg) return;

      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-label', 'Africa risk heat map preview');

      // Anchor Kenya as home base — gold stroke + glow handled in CSS.
      const ken = svg.querySelector('path[data-iso="KEN"]');
      if (ken) ken.classList.add('is-anchor');
    } catch (err) {
      container.innerHTML = '<p style="color:var(--color-ink-low);font-family:var(--font-mono);font-size:12px;letter-spacing:.08em;text-align:center">Map preview unavailable.</p>';
      console.error('Home Africa teaser failed:', err);
    }
  }
})();
