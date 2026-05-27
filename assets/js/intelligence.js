/* =========================================================================
   GTS RISK ADVISORY  ·  INTELLIGENCE PRODUCTS
   Renders the five intelligence-product sections on /intelligence/ from
   /data/intelligence.json. Layout alternates (split / split--reverse) based
   on position. The Risk Heat Map product gets an extra CTA from its `cta`
   field.
   ========================================================================= */

(function () {
  'use strict';

  const ENDPOINT = '/data/intelligence.json';

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // Short anchor aliases used by the global Intelligence nav dropdown.
  // The full canonical id stays "product-<slug>"; these aliases let menu
  // links like /intelligence/#reports scroll to the right section.
  const ANCHOR_ALIAS = {
    'intelligence-reports':     'reports',
    'political-country-risk':   'political',
    'daily-monitoring-briefs':  'monitoring',
    'situational-risk-analysis':'situational',
    'risk-heat-map':            'heatmap',
  };

  // Note: p.number is retained in intelligence.json but intentionally not
  // rendered (the "Product NN" eyebrow was removed). Re-add a one-line
  // <span class="eyebrow">Product ${p.number}</span> above the <h2> to restore.
  function productMarkup(p, idx) {
    const splitClass = idx % 2 === 0 ? 'split' : 'split split--reverse';
    const bodyHtml = (p.body || []).map((para) => `<p>${escapeHtml(para)}</p>`).join('');
    const ctaHtml = p.cta && p.cta.href && p.cta.label
      ? `<div class="mt-5"><a href="${escapeHtml(p.cta.href)}" class="btn btn--primary">${escapeHtml(p.cta.label)} →</a></div>`
      : '';
    const stamp = p.classified_stamp ? `<span class="stamp">${escapeHtml(p.classified_stamp)}</span>` : '';
    const altText = `Visual reference for ${p.name}`;
    const alias = ANCHOR_ALIAS[p.slug];
    const aliasAnchor = alias ? `<span id="${escapeHtml(alias)}" class="anchor-alias" aria-hidden="true"></span>` : '';

    return `
      ${aliasAnchor}
      <article class="product-block" id="product-${escapeHtml(p.slug)}">
        <div class="container">
          <div class="${splitClass}">
            <div class="reveal">
              <h2 style="margin-top:var(--s-3);margin-bottom:var(--s-4);">${escapeHtml(p.name)}</h2>
              <p class="lede mb-5">${escapeHtml(p.lede)}</p>
              ${bodyHtml}
              ${ctaHtml}
            </div>
            <div class="product-preview reveal" data-delay="1">
              <picture>
                ${p.image_webp ? `<source srcset="${escapeHtml(p.image_webp)}" type="image/webp">` : ''}
                <img src="${escapeHtml(p.image)}" alt="${escapeHtml(altText)}" loading="lazy" decoding="async">
              </picture>
              ${stamp}
            </div>
          </div>
        </div>
      </article>
    `;
  }

  function rebindReveals(scope) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches
        || !('IntersectionObserver' in window)) {
      scope.querySelectorAll('.reveal').forEach((el) => el.classList.add('is-in-view'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
    scope.querySelectorAll('.reveal').forEach((el) => io.observe(el));
  }

  document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('intel-products');
    if (!container) return;
    try {
      const res = await fetch(ENDPOINT);
      if (!res.ok) throw new Error('intelligence.json ' + res.status);
      const data = await res.json();
      const products = Array.isArray(data.products) ? data.products : [];
      container.innerHTML = products.map(productMarkup).join('');
      rebindReveals(container);
    } catch (err) {
      console.error('Intelligence products failed to load:', err);
    }
  });
})();
