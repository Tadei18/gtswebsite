/* =========================================================================
   GTS RISK ADVISORY  ·  LEADERSHIP GRID
   Fetches /data/team.json and renders the leader cards.
   If a member has a `photo` path, renders a <picture> (WebP + JPG).
   Otherwise renders an animated monogram placeholder.
   To swap a placeholder for a real photo: edit team.json — no HTML touched.
   ========================================================================= */

(function () {
  'use strict';

  const ENDPOINT = '/data/team.json';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /** "James Otieno" -> "JO"; max 3 initials. */
  function initials(name) {
    return name
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 3)
      .map((w) => w[0].toUpperCase())
      .join('');
  }

  function photoMarkup(photo, name) {
    const webp = photo.replace(/\.(jpe?g|png)$/i, '.webp');
    return `
      <div class="leader__portrait">
        <picture>
          <source srcset="${escapeHtml(webp)}" type="image/webp">
          <img src="${escapeHtml(photo)}" alt="Portrait of ${escapeHtml(name)}" loading="lazy" decoding="async">
        </picture>
      </div>
    `;
  }

  function monogramMarkup(name) {
    const ini = escapeHtml(initials(name));
    const safeName = escapeHtml(name);
    // L-shaped corner brackets — one SVG path per corner, viewBox 12x12,
    // path length ~21 (used as stroke-dasharray for the draw-in animation).
    return `
      <div class="monogram" role="img" aria-label="Portrait placeholder for ${safeName}">
        <span class="monogram__initials" aria-hidden="true">${ini}</span>
        <span class="monogram__rule" aria-hidden="true"></span>
        <svg class="monogram__bracket monogram__bracket--tl" viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 12 L1.5 1.5 L12 1.5"/></svg>
        <svg class="monogram__bracket monogram__bracket--tr" viewBox="0 0 12 12" aria-hidden="true"><path d="M0 1.5 L10.5 1.5 L10.5 12"/></svg>
        <svg class="monogram__bracket monogram__bracket--br" viewBox="0 0 12 12" aria-hidden="true"><path d="M10.5 0 L10.5 10.5 L0 10.5"/></svg>
        <svg class="monogram__bracket monogram__bracket--bl" viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 0 L1.5 10.5 L12 10.5"/></svg>
      </div>
    `;
  }

  function cardMarkup(m, idx) {
    const portrait = m.photo ? photoMarkup(m.photo, m.name) : monogramMarkup(m.name);
    const delay = Math.min(idx + 1, 4); // matches existing .reveal[data-delay="N"] support (1–4)
    return `
      <div class="leader reveal" data-delay="${delay}">
        ${portrait}
        <span class="leader__role">${escapeHtml(m.role)}</span>
        <h3 class="leader__name">${escapeHtml(m.name)}</h3>
        <p class="leader__bio">${escapeHtml(m.bio)}</p>
      </div>
    `;
  }

  /** Local reveal observer for cards injected after main.js's reveal pass. */
  function observeCards(cards) {
    if (prefersReducedMotion) {
      cards.forEach((el) => el.classList.add('is-in-view'));
      return;
    }
    if (!('IntersectionObserver' in window)) {
      cards.forEach((el) => el.classList.add('is-in-view'));
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
    cards.forEach((el) => io.observe(el));
  }

  document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('leaders-grid');
    if (!grid) return;
    try {
      const res = await fetch(ENDPOINT);
      if (!res.ok) throw new Error('team.json ' + res.status);
      const data = await res.json();
      if (!data || !Array.isArray(data.team)) throw new Error('team.json shape invalid');

      grid.innerHTML = data.team.map(cardMarkup).join('');
      observeCards(Array.from(grid.querySelectorAll('.leader')));
    } catch (err) {
      // Leave the grid empty — page remains usable.
      console.error('Leadership grid failed to load:', err);
    }
  });
})();
