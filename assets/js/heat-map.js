/* =========================================================================
   GTS RISK ADVISORY  ·  HEAT MAP
   Africa risk heat map — real-geography SVG, hover tooltip, click-to-dossier
   panel, filters. Mobile uses a vertical list fallback (see initMobile).
   Depends on assets/js/africa-map.js for the shared loader.
   ========================================================================= */

(function () {
  'use strict';

  const MOBILE_BREAKPOINT = 900;

  const STATE = {
    countries: null,           // map of iso → country
    selectedIso: null,
    filters: { region: '', risk: '', search: '' },
  };

  /* -------------------------------------------------------------- */
  /*  Boot                                                          */
  /* -------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', async () => {
    const canvas = document.getElementById('heatmap-canvas');
    if (!canvas) return;
    if (!window.GTSAfricaMap) {
      console.error('GTSAfricaMap loader missing.');
      return;
    }

    try {
      const data = await window.GTSAfricaMap.loadHeatMapData();
      STATE.countries = {};
      data.countries.forEach((c) => { STATE.countries[c.iso] = c; });

      if (window.innerWidth < MOBILE_BREAKPOINT) {
        renderMobileList(canvas);
      } else {
        await renderMap(canvas);
      }
      bindFilters();
    } catch (err) {
      canvas.innerHTML = '<p style="color:var(--color-ink-low);font-family:var(--font-mono);font-size:14px;letter-spacing:.08em">Unable to load heat-map data. Serve the site over HTTP (e.g. <code>python -m http.server</code>) to enable JSON loading.</p>';
      console.error('Heat-map data load failed:', err);
    }
  });

  /* -------------------------------------------------------------- */
  /*  Render real Africa SVG                                        */
  /* -------------------------------------------------------------- */
  async function renderMap(canvas) {
    const svg = await window.GTSAfricaMap.injectMap(canvas, STATE.countries);
    if (!svg) return;

    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Africa risk heat map');

    svg.querySelectorAll('path.country').forEach((p) => {
      const iso = p.getAttribute('data-iso');
      const c = STATE.countries[iso];
      if (!c) return;
      p.setAttribute('tabindex', '0');
      p.setAttribute('role', 'button');
      p.setAttribute('aria-label', `${c.name} — ${c.risk} risk`);
      bindCountry(p, c);
    });
  }

  /* -------------------------------------------------------------- */
  /*  Mobile fallback — vertical list grouped by region             */
  /* -------------------------------------------------------------- */
  function renderMobileList(canvas) {
    const byRegion = {};
    Object.values(STATE.countries).forEach((c) => {
      const r = c.region || 'Other';
      (byRegion[r] = byRegion[r] || []).push(c);
    });
    Object.keys(byRegion).forEach((r) => {
      byRegion[r].sort((a, b) => a.name.localeCompare(b.name));
    });

    const html = Object.keys(byRegion).sort().map((region) => `
      <div class="heatmap-mobile__group" data-region="${region}">
        <div class="heatmap-mobile__region">${region}</div>
        <div class="heatmap-mobile__cards">
          ${byRegion[region].map((c) => `
            <button class="heatmap-mobile__card" data-iso="${c.iso}" data-risk="${c.risk}">
              <span class="heatmap-mobile__name">${c.name}</span>
              <span class="chip chip--risk chip--risk-${c.risk}">${c.risk}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `).join('');

    canvas.innerHTML = `<div class="heatmap-mobile">${html}</div>`;
    canvas.querySelectorAll('.heatmap-mobile__card').forEach((btn) => {
      btn.addEventListener('click', () => {
        const c = STATE.countries[btn.getAttribute('data-iso')];
        if (c) openDossier(c);
      });
    });
  }

  /* -------------------------------------------------------------- */
  /*  Country interactions                                          */
  /* -------------------------------------------------------------- */
  function bindCountry(el, country) {
    const tooltip = document.getElementById('heatmap-tooltip');
    el.addEventListener('mousemove', (e) => showTooltip(tooltip, country, e.clientX, e.clientY));
    el.addEventListener('mouseleave', () => hideTooltip(tooltip));
    el.addEventListener('focus', () => {
      const r = el.getBoundingClientRect();
      showTooltip(tooltip, country, r.left + r.width / 2, r.top);
    });
    el.addEventListener('blur', () => hideTooltip(tooltip));
    el.addEventListener('click', () => openDossier(country));
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openDossier(country);
      }
    });
  }

  function showTooltip(tt, c, x, y) {
    if (!tt) return;
    tt.innerHTML = `
      <div class="heatmap-tooltip__iso">— ${c.iso} · ${c.region || 'N/A'}</div>
      <div class="heatmap-tooltip__name">${c.name}</div>
      <div class="heatmap-tooltip__summary">${c.summary || 'Detailed dossier available to subscribers.'}</div>
      <div style="margin-top:8px"><span class="chip chip--risk chip--risk-${c.risk}">${c.risk}</span></div>
    `;
    tt.style.left = (x + 16) + 'px';
    tt.style.top  = (y + 16) + 'px';
    tt.classList.add('is-visible');
    tt.setAttribute('aria-hidden', 'false');
  }

  function hideTooltip(tt) {
    if (!tt) return;
    tt.classList.remove('is-visible');
    tt.setAttribute('aria-hidden', 'true');
  }

  /* -------------------------------------------------------------- */
  /*  Dossier panel                                                 */
  /* -------------------------------------------------------------- */
  function openDossier(c) {
    STATE.selectedIso = c.iso;
    const panel = document.getElementById('heatmap-dossier');
    if (!panel) return;

    const hasDetail = c.overview && c.key_risks && c.outlook && c.recommendations;
    const scoreLabels = { security: 'Security', political: 'Political', economic: 'Economic', operational: 'Operational' };
    const scoresHtml = c.scores ? Object.keys(c.scores).map(k => `
      <div class="score">
        <div class="score__label">
          <span>${scoreLabels[k] || k}</span><span class="val">${c.scores[k]}/5</span>
        </div>
        <div class="score__track">
          <span class="score__fill" data-fill="${(c.scores[k]/5)*100}"></span>
        </div>
      </div>`).join('') : '';

    let tabsHtml = '';
    if (hasDetail) {
      tabsHtml = `
        <div class="tabs">
          <div class="tabs__list" role="tablist">
            <button class="tabs__tab is-active" data-tab="overview" role="tab">Overview</button>
            <button class="tabs__tab" data-tab="risks" role="tab">Key Risks</button>
            <button class="tabs__tab" data-tab="outlook" role="tab">Outlook</button>
            <button class="tabs__tab" data-tab="rec" role="tab">Recommendations</button>
          </div>
          <div class="tabs__panel is-active" data-panel="overview"><p style="color:var(--color-ink-mid);line-height:1.65">${c.overview}</p></div>
          <div class="tabs__panel" data-panel="risks"><ul class="bullet-list">${c.key_risks.map(r => '<li>' + r + '</li>').join('')}</ul></div>
          <div class="tabs__panel" data-panel="outlook"><p style="color:var(--color-ink-mid);line-height:1.65">${c.outlook}</p></div>
          <div class="tabs__panel" data-panel="rec"><ul class="bullet-list">${c.recommendations.map(r => '<li>' + r + '</li>').join('')}</ul></div>
        </div>`;
    } else {
      tabsHtml = `<p style="color:var(--color-ink-mid);line-height:1.65;padding:var(--s-5);background:var(--color-surface-2);border:1px solid var(--color-border);border-top:1px solid var(--color-gold)"><em>${c.summary || 'Detailed dossier coverage in development.'}</em><br><br>Full country dossier — overview, key risks, outlook, and recommendations — available to subscribers. <a href="/contact/" style="color:var(--color-gold)">Contact us</a> to request access.</p>`;
    }

    panel.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:var(--s-3);margin-bottom:var(--s-4)">
        <div>
          <span class="eyebrow">${c.iso} · ${c.region || 'N/A'}</span>
          <h2 style="margin-top:var(--s-2);font-size:1.75rem">${c.name}</h2>
        </div>
        <span class="risk-pill chip--risk chip--risk-${c.risk}">${c.risk}</span>
      </div>
      <div class="heatmap-dossier__scores">${scoresHtml}</div>
      ${tabsHtml}
      <div style="margin-top:var(--s-6);padding-top:var(--s-5);border-top:1px solid var(--color-border)">
        <a href="/contact/" class="btn btn--primary btn--block">Request full country report →</a>
      </div>
    `;

    // Animate score fills
    requestAnimationFrame(() => {
      panel.querySelectorAll('.score__fill').forEach((s) => {
        s.style.width = s.getAttribute('data-fill') + '%';
      });
    });

    // Bind tabs
    panel.querySelectorAll('.tabs__tab').forEach((tab) => {
      tab.addEventListener('click', () => {
        const key = tab.getAttribute('data-tab');
        panel.querySelectorAll('.tabs__tab').forEach((t) => t.classList.toggle('is-active', t === tab));
        panel.querySelectorAll('.tabs__panel').forEach((p) => p.classList.toggle('is-active', p.getAttribute('data-panel') === key));
      });
    });

    if (window.innerWidth < MOBILE_BREAKPOINT) {
      panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  /* -------------------------------------------------------------- */
  /*  Filters                                                       */
  /* -------------------------------------------------------------- */
  function bindFilters() {
    const search = document.getElementById('heatmap-search');
    const region = document.getElementById('heatmap-region');
    const risk = document.getElementById('heatmap-risk');

    if (search) search.addEventListener('input', () => { STATE.filters.search = search.value.toLowerCase().trim(); applyFilters(); });
    if (region) region.addEventListener('change', () => { STATE.filters.region = region.value; applyFilters(); });
    if (risk)   risk.addEventListener('change',   () => { STATE.filters.risk   = risk.value;   applyFilters(); });
  }

  function applyFilters() {
    const isVisible = (c) => {
      if (!c) return false;
      const matchRegion = !STATE.filters.region || c.region === STATE.filters.region;
      const matchRisk   = !STATE.filters.risk   || c.risk === STATE.filters.risk;
      const q = STATE.filters.search;
      const matchSearch = !q || c.name.toLowerCase().includes(q) || c.iso.toLowerCase().includes(q);
      return matchRegion && matchRisk && matchSearch;
    };

    // Desktop SVG paths
    document.querySelectorAll('.heatmap-canvas path.country').forEach((p) => {
      const c = STATE.countries[p.getAttribute('data-iso')];
      const v = isVisible(c);
      p.style.opacity = v ? '1' : '0.12';
      p.style.pointerEvents = v ? 'auto' : 'none';
    });

    // Mobile list cards
    document.querySelectorAll('.heatmap-mobile__card').forEach((btn) => {
      const c = STATE.countries[btn.getAttribute('data-iso')];
      btn.style.display = isVisible(c) ? '' : 'none';
    });
    document.querySelectorAll('.heatmap-mobile__group').forEach((g) => {
      const visibleCount = g.querySelectorAll('.heatmap-mobile__card:not([style*="display: none"])').length;
      g.style.display = visibleCount === 0 ? 'none' : '';
    });
  }
})();
