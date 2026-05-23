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
      JOBS = data.jobs;
    } catch (err) {
      console.error('Could not load jobs.json:', err);
      JOBS = [];
    }

    bindFilters();
    bindRowClicks();
    bindModalClose();
  });

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
