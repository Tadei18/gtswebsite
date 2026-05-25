/* =========================================================================
   GTS RISK ADVISORY  ·  CAREERS
   Filter open roles + render application modal.
   ========================================================================= */

(function () {
  'use strict';

  let JOBS = [];

  document.addEventListener('DOMContentLoaded', async () => {
    const list = document.getElementById('job-list');
    if (!list) return;

    try {
      const res = await fetch('/data/jobs.json');
      const data = await res.json();
      JOBS = Array.isArray(data.jobs) ? data.jobs : [];
    } catch (err) {
      console.error('Could not load jobs.json:', err);
      JOBS = [];
    }

    if (JOBS.length === 0) {
      renderNoOpenings(list);
      return; // no filters, no rows, no modal needed
    }

    renderRows(list);
    bindFilters();
    bindRowClicks();
    bindModalClose();
  });

  function renderNoOpenings(list) {
    // Hide the (now-pointless) filter/search UI.
    const filters = document.getElementById('job-filters');
    if (filters) filters.style.display = 'none';

    list.classList.add('job-list--empty');
    list.innerHTML = `
      <div class="no-openings">
        <span class="eyebrow">Currently</span>
        <h3 class="no-openings__title">No active openings at this time.</h3>
        <p class="no-openings__body">We continue to build our team as engagements grow. If your background aligns with our practice areas — corporate security, risk advisory, intelligence analysis, or operations — we welcome expressions of interest for future consideration.</p>
        <a href="#general-application" class="btn btn--primary no-openings__cta">Submit a general application →</a>
      </div>
    `;

    const cta = list.querySelector('.no-openings__cta');
    if (cta) {
      cta.addEventListener('click', (e) => {
        const target = document.getElementById('general-application');
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          const focusable = target.querySelector('a, button');
          if (focusable) focusable.focus({ preventScroll: true });
        }
      });
    }
  }

  function renderRows(list) {
    list.innerHTML = JOBS.map((job) => `
      <a class="job-row" href="#job-${job.id}" data-job="${job.id}">
        <div class="job-row__title">${job.title}</div>
        <div class="job-row__dept">${job.department}</div>
        <div class="job-row__loc">${job.location}</div>
        <div class="job-row__cta">View role →</div>
      </a>
    `).join('');
  }

  function bindFilters() {
    const dept = document.getElementById('job-filter-dept');
    const loc  = document.getElementById('job-filter-loc');
    const q    = document.getElementById('job-filter-search');

    const apply = () => {
      const dv = dept ? dept.value : '';
      const lv = loc ? loc.value : '';
      const qv = q ? q.value.toLowerCase().trim() : '';
      document.querySelectorAll('#job-list .job-row').forEach((row) => {
        const department = row.querySelector('.job-row__dept').textContent.trim();
        const location   = row.querySelector('.job-row__loc').textContent.trim();
        const title      = row.querySelector('.job-row__title').textContent.toLowerCase();
        const matchDept = !dv || department === dv;
        const matchLoc  = !lv || location === lv;
        const matchQ    = !qv || title.includes(qv);
        row.style.display = matchDept && matchLoc && matchQ ? '' : 'none';
      });
    };

    if (dept) dept.addEventListener('change', apply);
    if (loc)  loc.addEventListener('change', apply);
    if (q)    q.addEventListener('input', apply);
  }

  function bindRowClicks() {
    document.querySelectorAll('#job-list .job-row').forEach((row) => {
      row.addEventListener('click', (e) => {
        e.preventDefault();
        const id = row.getAttribute('data-job');
        const job = JOBS.find((j) => j.id === id);
        if (job) openModal(job);
      });
    });
  }

  function openModal(job) {
    const modal = document.getElementById('job-modal');
    const content = document.getElementById('job-modal-content');
    if (!modal || !content) return;

    const responsibilities = job.responsibilities.map((r) => `<li>${r}</li>`).join('');
    const requirements = job.requirements.map((r) => `<li>${r}</li>`).join('');

    content.innerHTML = `
      <span class="eyebrow">${job.department} · ${job.location} · ${job.type}</span>
      <h2 id="job-modal-title" style="margin:var(--s-3) 0 var(--s-4)">${job.title}</h2>
      <p style="color:var(--color-ink-mid);line-height:1.65;margin-bottom:var(--s-6)">${job.summary}</p>

      <h3 style="margin-bottom:var(--s-3);font-size:1.125rem">Responsibilities</h3>
      <ul class="bullet-list mb-6">${responsibilities}</ul>

      <h3 style="margin-bottom:var(--s-3);font-size:1.125rem">Requirements</h3>
      <ul class="bullet-list mb-6">${requirements}</ul>

      <div style="border-top:1px solid var(--color-border);padding-top:var(--s-5);margin-top:var(--s-5)">
        <h3 style="margin-bottom:var(--s-4);font-size:1.125rem">Apply</h3>
        <form class="form" action="https://formsubmit.co/info@gtsriskadvisory.com" method="POST" enctype="multipart/form-data" novalidate>
          <input type="hidden" name="_subject" value="Application — ${job.title}">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="true">
          <input type="hidden" name="_next" value="/contact/thank-you.html">
          <input type="hidden" name="position" value="${job.title}">
          <input type="text" name="_honey" class="honeypot" autocomplete="off" tabindex="-1">

          <div class="form-row">
            <div class="field">
              <input type="text" name="name" id="a-name" required placeholder=" " class="field__input">
              <label for="a-name" class="field__label">Full name *</label>
            </div>
            <div class="field">
              <input type="email" name="email" id="a-email" required placeholder=" " class="field__input">
              <label for="a-email" class="field__label">Email *</label>
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <input type="tel" name="phone" id="a-phone" required placeholder=" " class="field__input">
              <label for="a-phone" class="field__label">Phone *</label>
            </div>
            <div class="field">
              <label style="position:static;color:var(--color-gold);font-family:var(--font-sans);font-size:var(--t-eyebrow);font-weight:600;letter-spacing:.16em;text-transform:uppercase;display:block;margin-bottom:8px">CV / Résumé *</label>
              <input type="file" name="cv" required accept=".pdf,.doc,.docx" style="color:var(--color-ink-mid);font-size:var(--t-small)">
            </div>
          </div>
          <div class="field">
            <textarea name="cover_note" id="a-cover" placeholder=" " class="field__textarea"></textarea>
            <label for="a-cover" class="field__label">Cover note (1–2 paragraphs)</label>
          </div>
          <div class="form__actions">
            <button type="submit" class="btn btn--primary">Submit application</button>
            <p style="font-size:var(--t-xs);color:var(--color-ink-low);margin:0">All applications are reviewed confidentially.</p>
          </div>
        </form>
      </div>
    `;

    modal.classList.add('is-open');
    document.body.classList.add('body-locked');
  }

  function bindModalClose() {
    const modal = document.getElementById('job-modal');
    if (!modal) return;
    const close = modal.querySelector('.modal__close');
    if (close) close.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });
  }

  function closeModal() {
    document.getElementById('job-modal').classList.remove('is-open');
    document.body.classList.remove('body-locked');
  }
})();
