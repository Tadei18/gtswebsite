/* =========================================================================
   GTS RISK ADVISORY  ·  HEAT MAP
   Africa risk heat map — tile-grid SVG, hover tooltip, click-to-dossier
   panel, filters, mobile responsive.
   ========================================================================= */

(function () {
  'use strict';

  const TILE_SIZE = 56;
  const TILE_GAP = 4;
  const GRID = [
    // Row 0 — North Africa
    [null, null, null, 'MAR', 'DZA', 'TUN', 'LBY', 'EGY', null, null],
    // Row 1
    [null, null, 'ESH', 'MRT', null, 'MLI', 'NER', 'TCD', 'SDN', 'ERI'],
    // Row 2 — West Africa / Sahel
    [null, 'CPV', 'SEN', 'GMB', 'GIN', 'BFA', 'NGA', 'CAF', 'SSD', 'DJI'],
    // Row 3
    ['GNB', 'SLE', 'LBR', 'CIV', 'GHA', 'TGO', 'BEN', 'CMR', 'ETH', 'SOM'],
    // Row 4 — Central / East
    [null, null, null, null, null, 'GNQ', 'GAB', 'COG', 'UGA', 'KEN'],
    // Row 5
    [null, null, null, null, null, 'STP', null, 'COD', 'RWA', 'TZA'],
    // Row 6
    [null, null, null, null, null, null, 'AGO', 'ZMB', 'BDI', 'MWI'],
    // Row 7 — Southern Africa
    [null, null, null, null, null, null, 'NAM', 'ZWE', 'MOZ', 'MDG'],
    // Row 8
    [null, null, null, null, null, null, null, 'BWA', 'SWZ', 'MUS'],
    // Row 9
    [null, null, null, null, null, null, null, null, 'ZAF', 'LSO'],
  ];

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

    try {
      const res = await fetch('/data/heat-map.json');
      const data = await res.json();
      STATE.countries = {};
      data.countries.forEach((c) => { STATE.countries[c.iso] = c; });
      renderMap(canvas);
      bindFilters();
    } catch (err) {
      canvas.innerHTML = '<p style="color:var(--color-ink-low);font-family:var(--font-mono);font-size:14px;letter-spacing:.08em">Unable to load heat-map data. Serve the site over HTTP (e.g. <code>python -m http.server</code>) to enable JSON loading.</p>';
      console.error('Heat-map data load failed:', err);
    }
  });

  /* -------------------------------------------------------------- */
  /*  Render tile-grid SVG                                          */
  /* -------------------------------------------------------------- */
  function renderMap(canvas) {
    const cols = GRID[0].length;
    const rows = GRID.length;
    const w = cols * (TILE_SIZE + TILE_GAP);
    const h = rows * (TILE_SIZE + TILE_GAP);

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Africa risk heat map — tile grid');

    GRID.forEach((row, r) => {
      row.forEach((iso, c) => {
        if (!iso) return;
        const country = STATE.countries[iso];
        if (!country) return;
        const x = c * (TILE_SIZE + TILE_GAP);
        const y = r * (TILE_SIZE + TILE_GAP);
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('data-iso', iso);
        g.setAttribute('data-risk', country.risk);
        g.setAttribute('data-region', country.region);
        g.setAttribute('tabindex', '0');
        g.setAttribute('role', 'button');
        g.setAttribute('aria-label', `${country.name} — ${country.risk} risk`);
        g.style.cursor = 'pointer';

        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('class', 'country');
        rect.setAttribute('x', x);
        rect.setAttribute('y', y);
        rect.setAttribute('width', TILE_SIZE);
        rect.setAttribute('height', TILE_SIZE);
        rect.setAttribute('fill', riskColor(country.risk));
        g.appendChild(rect);

        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('class', 'country-label');
        label.setAttribute('x', x + TILE_SIZE / 2);
        label.setAttribute('y', y + TILE_SIZE / 2 + 4);
        label.textContent = iso;
        g.appendChild(label);

        bindTile(g, country);
        svg.appendChild(g);
      });
    });

    canvas.appendChild(svg);
  }

  function riskColor(r) {
    return {
      low:      'var(--risk-low)',
      moderate: 'var(--risk-moderate)',
      elevated: 'var(--risk-elevated)',
      high:     'var(--risk-high)',
      extreme:  'var(--risk-extreme)',
    }[r] || 'var(--risk-na)';
  }

  /* -------------------------------------------------------------- */
  /*  Tile interactions                                             */
  /* -------------------------------------------------------------- */
  function bindTile(g, country) {
    const tooltip = document.getElementById('heatmap-tooltip');
    g.addEventListener('mousemove', (e) => showTooltip(tooltip, country, e.clientX, e.clientY));
    g.addEventListener('mouseleave', () => hideTooltip(tooltip));
    g.addEventListener('focus', () => {
      const rect = g.getBoundingClientRect();
      showTooltip(tooltip, country, rect.left + rect.width / 2, rect.top);
    });
    g.addEventListener('blur', () => hideTooltip(tooltip));
    g.addEventListener('click', () => openDossier(country));
    g.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openDossier(country);
      }
    });
  }

  function showTooltip(tt, c, x, y) {
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

    // Scroll panel into view on mobile
    if (window.innerWidth < 900) {
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
    document.querySelectorAll('.heatmap-canvas g[data-iso]').forEach((g) => {
      const iso = g.getAttribute('data-iso');
      const c = STATE.countries[iso];
      const matchRegion = !STATE.filters.region || c.region === STATE.filters.region;
      const matchRisk   = !STATE.filters.risk   || c.risk === STATE.filters.risk;
      const q = STATE.filters.search;
      const matchSearch = !q || c.name.toLowerCase().includes(q) || c.iso.toLowerCase().includes(q);
      const visible = matchRegion && matchRisk && matchSearch;
      g.style.opacity = visible ? '1' : '0.15';
      g.style.pointerEvents = visible ? 'auto' : 'none';
    });
  }
})();
