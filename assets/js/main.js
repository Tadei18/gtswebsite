/* =========================================================================
   GTS RISK ADVISORY  ·  MAIN
   Partials loader (optional), sticky header, mobile nav, reveals,
   counter-ups, dropdowns.
   ========================================================================= */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* WhatsApp floating contact button — site-wide.
     To disable: set enabled: false. To change number/message: edit here. */
  const WHATSAPP_CONFIG = {
    number: '254722658301',                       // international format, no + or spaces
    message: "Hello GTS, I'd like to discuss",
    enabled: true,
    excludePaths: ['/contact/thank-you'],         // matched as prefixes
    revealDelayMs: 800,
  };

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
      // Past 80px: condense the header (shrinks the enlarged logo, tightens padding, adds blur).
      const next = window.scrollY > 80;
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
    const MARGIN = 16;

    // Nudge an open mega-menu back inside the viewport if its natural
    // (centered) position would clip either edge. Trigger-agnostic.
    function repositionDropdown(menu) {
      // Reset so we measure the natural centered position, not a stale offset.
      menu.style.transform = '';
      menu.style.maxWidth = '';

      // Fallback: if the panel can't fit at all, cap its width first.
      if (menu.getBoundingClientRect().width > window.innerWidth - MARGIN * 2) {
        menu.style.maxWidth = `calc(100vw - ${MARGIN * 2}px)`;
      }

      const rect = menu.getBoundingClientRect();
      let nudge = 0;
      if (rect.left < MARGIN) {
        nudge = MARGIN - rect.left;
      } else if (rect.right > window.innerWidth - MARGIN) {
        nudge = (window.innerWidth - MARGIN) - rect.right;
      }

      if (nudge !== 0) {
        // Preserve the centering transform; add the horizontal nudge on top.
        menu.style.transform = `translateX(calc(-50% + ${nudge}px)) translateY(0)`;
      }
    }

    function clearDropdown(menu) {
      menu.style.transform = '';
      menu.style.maxWidth = '';
    }

    items.forEach((item) => {
      const trigger = item.querySelector('.nav__link');
      const menu = item.querySelector('.dropdown');
      if (!menu || !trigger) return;

      // requestAnimationFrame lets the CSS open state commit before we measure.
      const scheduleReposition = () => requestAnimationFrame(() => repositionDropdown(menu));

      // Hover open is CSS-driven (:hover); we only reposition.
      item.addEventListener('mouseenter', scheduleReposition);
      item.addEventListener('mouseleave', () => { item.classList.remove('is-open'); clearDropdown(menu); });

      // Keyboard / focus open.
      trigger.addEventListener('focus', () => { item.classList.add('is-open'); scheduleReposition(); });
      item.addEventListener('focusout', (e) => {
        if (!item.contains(e.relatedTarget)) { item.classList.remove('is-open'); clearDropdown(menu); }
      });
    });

    // Reflow any currently-open dropdown on resize (debounced).
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        items.forEach((item) => {
          const menu = item.querySelector('.dropdown');
          if (!menu) return;
          const isOpen = item.classList.contains('is-open') || item.matches(':hover');
          if (isOpen) repositionDropdown(menu);
        });
      }, 100);
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
     9.  WhatsApp floating contact button — injected, single source of truth
     ----------------------------------------------------------------------- */
  function injectWhatsAppFab() {
    if (!WHATSAPP_CONFIG.enabled) return;
    if (document.querySelector('.wa-fab')) return; // idempotent

    // Path-based exclusion (e.g. /contact/thank-you).
    const path = window.location.pathname
      .replace(/\.html?$/, '')
      .replace(/\/index$/, '/')
      .replace(/\/$/, '/');
    const excluded = WHATSAPP_CONFIG.excludePaths.some((p) => {
      const n = p.replace(/\/$/, '/');
      return path === n || path.startsWith(n);
    });
    if (excluded) return;

    // Explicit opt-out per page: <body data-no-whatsapp>.
    if (document.body.hasAttribute('data-no-whatsapp')) return;

    const href = 'https://wa.me/' + encodeURIComponent(WHATSAPP_CONFIG.number) +
      '?text=' + encodeURIComponent(WHATSAPP_CONFIG.message);

    const fab = document.createElement('a');
    fab.className = 'wa-fab';
    fab.href = href;
    fab.target = '_blank';
    fab.rel = 'noopener noreferrer';
    fab.setAttribute('aria-label', 'Contact GTS on WhatsApp');
    fab.innerHTML = `
      <svg class="wa-fab__icon" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
        <path d="M20.52 3.48A11.86 11.86 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.9c0 2.1.55 4.14 1.6 5.95L0 24l6.32-1.66a11.93 11.93 0 0 0 5.73 1.46h.01c6.55 0 11.89-5.34 11.89-11.9a11.83 11.83 0 0 0-3.43-8.42M12.05 21.78h-.01a9.88 9.88 0 0 1-5.04-1.38l-.36-.22-3.74.98 1-3.65-.24-.37a9.88 9.88 0 0 1-1.51-5.24c0-5.46 4.45-9.9 9.9-9.9 2.65 0 5.14 1.03 7.01 2.9a9.86 9.86 0 0 1 2.9 7.01c0 5.46-4.45 9.9-9.91 9.9m5.43-7.41c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.95 1.17-.17.2-.35.22-.65.07-.3-.15-1.25-.46-2.38-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.21-.24-.58-.49-.5-.67-.51-.17 0-.37-.01-.57-.01-.2 0-.52.07-.79.37-.27.3-1.04 1.01-1.04 2.47 0 1.46 1.07 2.88 1.22 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.48 1.69.62.71.23 1.36.19 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35"/>
      </svg>
      <span class="wa-fab__tooltip" aria-hidden="true">Chat with GTS on WhatsApp</span>
    `;

    document.body.appendChild(fab);

    // Entrance: delay so it doesn't fight the hero on first paint.
    if (prefersReducedMotion) {
      fab.classList.add('is-revealed');
    } else {
      window.setTimeout(() => fab.classList.add('is-revealed'), WHATSAPP_CONFIG.revealDelayMs);
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
    injectWhatsAppFab();
  }

  document.addEventListener('DOMContentLoaded', async () => {
    await loadPartials();
    init();
    // Re-init after partials load (chrome may have been swapped in)
    document.addEventListener('partials:loaded', init);
  });
})();
