/* =========================================================================
   GTS RISK ADVISORY  ·  NAV POSTS
   Populates the Intelligence dropdown's right column (and the mobile-nav
   accordion's posts strip) with the 3 most-recent posts from posts.json.
   Cached in sessionStorage so subsequent page loads in the same session
   skip the network round-trip.
   ========================================================================= */

(function () {
  'use strict';

  const ENDPOINT = '/data/posts.json';
  const CACHE_KEY = 'gts:nav-posts:v1';
  const SKELETON_TIMEOUT_MS = 200;

  const desktopHost = document.getElementById('intel-dropdown-posts');
  const mobileHost  = document.getElementById('mobile-intel-posts');
  if (!desktopHost && !mobileHost) return;

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function fmtDate(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return '';
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();
  }

  function topThree(data) {
    const posts = Array.isArray(data && data.posts) ? data.posts.slice() : [];
    posts.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
    return posts.slice(0, 3);
  }

  function loadPosts() {
    try {
      const cached = sessionStorage.getItem(CACHE_KEY);
      if (cached) return Promise.resolve(JSON.parse(cached));
    } catch (_) { /* sessionStorage unavailable — fall through */ }

    return fetch(ENDPOINT).then((r) => {
      if (!r.ok) throw new Error('posts.json ' + r.status);
      return r.json();
    }).then((data) => {
      try { sessionStorage.setItem(CACHE_KEY, JSON.stringify(data)); } catch (_) {}
      return data;
    });
  }

  function renderDesktop(posts) {
    if (!desktopHost) return;
    if (!posts.length) return renderDesktopFallback();
    desktopHost.innerHTML = posts.map((p) => `
      <a class="dropdown__post" href="${escapeHtml(p.file)}">
        <span class="dropdown__post-meta">
          <span class="dropdown__post-cat">${escapeHtml(p.category || '')}</span>
          <span class="dropdown__post-date">${escapeHtml(fmtDate(p.date))}</span>
        </span>
        <span class="dropdown__post-title">${escapeHtml(p.title)}</span>
      </a>
    `).join('');
    desktopHost.removeAttribute('data-skeleton');
  }

  function renderDesktopFallback() {
    if (!desktopHost) return;
    desktopHost.innerHTML = `
      <p class="dropdown__posts-fallback">
        Latest insights from the GTS Intelligence Desk —
        <a href="/insights/">view all →</a>
      </p>
    `;
    desktopHost.removeAttribute('data-skeleton');
  }

  function renderMobile(posts) {
    if (!mobileHost) return;
    if (!posts.length) {
      mobileHost.innerHTML = '';
      return;
    }
    mobileHost.innerHTML = posts.map((p) => `
      <a class="mobile-nav__post" href="${escapeHtml(p.file)}">${escapeHtml(p.title)}</a>
    `).join('');
  }

  // Don't block the dropdown's open animation. Show skeleton after 200ms only
  // if we haven't resolved by then; that way a warm cache feels instant and a
  // cold cache reads as intentional, not janky.
  let resolved = false;
  const shimmerTimer = setTimeout(() => {
    if (!resolved && desktopHost) {
      desktopHost.classList.add('is-shimmering');
    }
  }, SKELETON_TIMEOUT_MS);

  loadPosts().then((data) => {
    resolved = true;
    clearTimeout(shimmerTimer);
    const posts = topThree(data);
    renderDesktop(posts);
    renderMobile(posts);
  }).catch((err) => {
    resolved = true;
    clearTimeout(shimmerTimer);
    console.error('nav-posts: failed to load', err);
    renderDesktopFallback();
    if (mobileHost) mobileHost.innerHTML = '';
  });
})();
