/* =========================================================================
   GTS RISK ADVISORY  ·  INSIGHTS
   Search, category filter, and pagination for the insights index.
   ========================================================================= */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('insights-grid');
    const search = document.getElementById('insights-search');
    const filterRow = document.getElementById('insights-filters');
    if (!grid) return;

    const cards = Array.from(grid.querySelectorAll('.post-card'));

    function apply(category, query) {
      const q = (query || '').toLowerCase().trim();
      cards.forEach((card) => {
        const text = card.textContent.toLowerCase();
        const cat = (card.querySelector('.post-card__cat') || {}).textContent || '';
        const matchCat = !category || cat.trim() === category;
        const matchQ = !q || text.includes(q);
        card.style.display = matchCat && matchQ ? '' : 'none';
      });
    }

    let activeCat = '';

    if (search) {
      search.addEventListener('input', () => apply(activeCat, search.value));
    }

    if (filterRow) {
      filterRow.querySelectorAll('.chip').forEach((chip) => {
        chip.addEventListener('click', (e) => {
          e.preventDefault();
          filterRow.querySelectorAll('.chip').forEach((c) => c.classList.remove('is-active'));
          chip.classList.add('is-active');
          activeCat = chip.getAttribute('data-cat') || '';
          apply(activeCat, search ? search.value : '');
        });
      });
    }
  });
})();
