/* =========================================================================
   GTS RISK ADVISORY  ·  MEDIA / GALLERY
   Category filtering + lightbox.
   ========================================================================= */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    bindFilters();
    bindLightbox();
  });

  function bindFilters() {
    const row = document.getElementById('media-filters');
    if (!row) return;
    row.querySelectorAll('.chip').forEach((chip) => {
      chip.addEventListener('click', (e) => {
        e.preventDefault();
        row.querySelectorAll('.chip').forEach((c) => c.classList.remove('is-active'));
        chip.classList.add('is-active');
        const filter = chip.getAttribute('data-filter');
        document.querySelectorAll('.gallery__item').forEach((item) => {
          const visible = filter === 'all' || item.getAttribute('data-cat') === filter;
          item.classList.toggle('is-visible', visible);
        });
      });
    });
  }

  let lightboxItems = [];
  let lightboxIndex = 0;

  function bindLightbox() {
    const lb = document.getElementById('lightbox');
    if (!lb) return;
    const img = document.getElementById('lightbox-img');
    const cap = document.getElementById('lightbox-caption');
    const close = lb.querySelector('.lightbox__close');
    const prev = lb.querySelector('.lightbox__prev');
    const next = lb.querySelector('.lightbox__next');

    function refreshList() {
      lightboxItems = Array.from(document.querySelectorAll('.gallery__item.is-visible'));
    }

    document.querySelectorAll('.gallery__item').forEach((item) => {
      item.addEventListener('click', () => {
        refreshList();
        lightboxIndex = lightboxItems.indexOf(item);
        if (lightboxIndex < 0) lightboxIndex = 0;
        show();
        lb.classList.add('is-open');
        document.body.classList.add('body-locked');
      });
    });

    function show() {
      const item = lightboxItems[lightboxIndex];
      if (!item) return;
      const src = item.querySelector('img').src;
      const caption = item.getAttribute('data-caption') || '';
      img.src = src;
      img.alt = caption;
      cap.textContent = caption;
    }

    function shut() {
      lb.classList.remove('is-open');
      document.body.classList.remove('body-locked');
    }

    function step(delta) {
      if (!lightboxItems.length) return;
      lightboxIndex = (lightboxIndex + delta + lightboxItems.length) % lightboxItems.length;
      show();
    }

    close.addEventListener('click', shut);
    prev.addEventListener('click', () => step(-1));
    next.addEventListener('click', () => step(1));
    lb.addEventListener('click', (e) => { if (e.target === lb) shut(); });
    document.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape')     shut();
      if (e.key === 'ArrowLeft')  step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
  }
})();
