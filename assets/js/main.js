/* =========================================================================
   GTS RISK ADVISORY  ·  MAIN
   Partials loader (optional), sticky header, mobile nav, reveals,
   counter-ups, dropdowns.
   ========================================================================= */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* -----------------------------------------------------------------------
     1.  Optional partials loader
     If a page uses <div data-include="/partials/x.html"></div>, fetch and
     inject it. Falls back silently when fetch fails (e.g. file:// protocol).
     ----------------------------------------------------------------------- */
  async function loadPartials() {
    const slots = document.querySelectorAll('[data-include]');
    if (!slots.length) return;
    for (const slot of slots) {
      const url = slot.getAttribute('data-include');
      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(res.status);
        slot.innerHTML = await res.text();
      } catch (err) {
        // Silent fail — keep the inline fallback the page already has.
        slot.removeAttribute('data-include');
      }
    }
    document.dispatchEvent(new CustomEvent('partials:loaded'));
  }

  /* -----------------------------------------------------------------------
     2.  Sticky header — backdrop-blur on scroll
     ----------------------------------------------------------------------- */
  function bindStickyHeader() {
    const header = document.getElementById('site-header');
    if (!header) return;
    let scrolled = false;
    const onScroll = () => {
      const next = window.scrollY > 24;
      if (next !== scrolled) {
        scrolled = next;
        header.classList.toggle('is-scrolled', scrolled);
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* -----------------------------------------------------------------------
     3.  Mobile nav — slide-in panel + scrim + body lock + focus trap
     ----------------------------------------------------------------------- */
  function bindMobileNav() {
    const toggle = document.querySelector('.nav-toggle');
    const panel  = document.getElementById('mobile-nav');
    const scrim  = document.getElementById('nav-scrim');
    const close  = panel ? panel.querySelector('.mobile-nav__close') : null;
    if (!toggle || !panel || !scrim || !close) return;

    const open = () => {
      panel.classList.add('is-open');
      scrim.classList.add('is-active');
      document.body.classList.add('body-locked');
      panel.setAttribute('aria-hidden', 'false');
      toggle.setAttribute('aria-expanded', 'true');
      // Focus first link
      const firstLink = panel.querySelector('a, button');
      if (firstLink) firstLink.focus();
    };
    const closeFn = () => {
      panel.classList.remove('is-open');
      scrim.classList.remove('is-active');
      document.body.classList.remove('body-locked');
      panel.setAttribute('aria-hidden', 'true');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    };

    toggle.addEventListener('click', open);
    close.addEventListener('click', closeFn);
    scrim.addEventListener('click', closeFn);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) closeFn();
    });

    // Close on link click (so navigation feels right)
    panel.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => {
        // give it a beat so the click registers
        setTimeout(closeFn, 80);
      });
    });
  }

  /* -----------------------------------------------------------------------
     4.  Desktop dropdown — keyboard support (hover handled by CSS)
     ----------------------------------------------------------------------- */
  function bindDropdowns() {
    const items = document.querySelectorAll('.nav__item');
    items.forEach((item) => {
      const trigger = item.querySelector('.nav__link');
      const menu = item.querySelector('.dropdown');
      if (!menu || !trigger) return;
      trigger.addEventListener('focus', () => item.classList.add('is-open'));
      item.addEventListener('mouseleave', () => item.classList.remove('is-open'));
      item.addEventListener('focusout', (e) => {
        if (!item.contains(e.relatedTarget)) item.classList.remove('is-open');
      });
    });
  }

  /* -----------------------------------------------------------------------
     5.  Reveal-on-scroll
     ----------------------------------------------------------------------- */
  function bindReveals() {
    const els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    if (prefersReducedMotion) {
      els.forEach((el) => el.classList.add('is-in-view'));
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
    els.forEach((el) => io.observe(el));
  }

  /* -----------------------------------------------------------------------
     6.  Counter-up — for hero metrics
     ----------------------------------------------------------------------- */
  function bindCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    if (!counters.length) return;
    if (prefersReducedMotion) {
      counters.forEach((c) => {
        const target = parseFloat(c.getAttribute('data-target'));
        c.textContent = formatNumber(target);
      });
      return;
    }
    const animate = (el) => {
      const target = parseFloat(el.getAttribute('data-target'));
      const duration = 1600;
      const start = performance.now();
      const ease = (t) => 1 - Math.pow(1 - t, 3);
      const step = (now) => {
        const t = Math.min((now - start) / duration, 1);
        const v = target * ease(t);
        el.textContent = formatNumber(v, target);
        if (t < 1) requestAnimationFrame(step);
        else el.textContent = formatNumber(target);
      };
      requestAnimationFrame(step);
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach((c) => io.observe(c));
  }

  function formatNumber(v, target) {
    const rounded = Math.floor(v);
    return rounded.toLocaleString('en-US');
  }

  /* -----------------------------------------------------------------------
     7.  Newsletter form — light validation, prevent default if email empty
     ----------------------------------------------------------------------- */
  function bindNewsletter() {
    const forms = document.querySelectorAll('.footer__newsletter');
    forms.forEach((form) => {
      form.addEventListener('submit', (e) => {
        const email = form.querySelector('input[type="email"]').value.trim();
        if (!email || !/^\S+@\S+\.\S+$/.test(email)) {
          e.preventDefault();
          form.querySelector('input').focus();
        }
      });
    });
  }

  /* -----------------------------------------------------------------------
     8.  Active nav highlight (matches current page)
     ----------------------------------------------------------------------- */
  function highlightActiveNav() {
    const path = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '/');

    const matches = (prefix) => {
      if (!prefix) return false;
      const n = prefix.replace(/\/index\.html$/, '/').replace(/\/$/, '/');
      return path === n || (n !== '/' && path.startsWith(n));
    };

    document.querySelectorAll('.nav__link, .mobile-nav__link').forEach((a) => {
      const href = a.getAttribute('href');
      // `data-active-paths` lets one nav item own multiple URL prefixes
      // (e.g. the merged Intelligence dropdown covers both /intelligence/ and /insights/).
      const extra = (a.getAttribute('data-active-paths') || '')
        .split(',').map((s) => s.trim()).filter(Boolean);
      const prefixes = extra.length ? extra : (href ? [href] : []);
      if (prefixes.some(matches)) a.classList.add('is-active');
    });

    if (path === '/' || path === '') {
      const home = document.querySelector('.nav__link[href="/"]');
      if (home) home.classList.add('is-active');
    }
  }

  /* -----------------------------------------------------------------------
     INIT
     ----------------------------------------------------------------------- */
  function init() {
    bindStickyHeader();
    bindMobileNav();
    bindDropdowns();
    bindReveals();
    bindCounters();
    bindNewsletter();
    highlightActiveNav();
  }

  document.addEventListener('DOMContentLoaded', async () => {
    await loadPartials();
    init();
    // Re-init after partials load (chrome may have been swapped in)
    document.addEventListener('partials:loaded', init);
  });
})();
