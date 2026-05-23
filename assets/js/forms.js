/* =========================================================================
   GTS RISK ADVISORY  ·  FORMS
   Contact page tabs + client-side validation for FormSubmit forms.
   ========================================================================= */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    bindTabs();
    bindValidation();
  });

  function bindTabs() {
    document.querySelectorAll('.tabs').forEach((tabs) => {
      const tabBtns = tabs.querySelectorAll('.tabs__tab');
      const panels  = tabs.querySelectorAll('.tabs__panel');
      tabBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          const key = btn.getAttribute('data-tab');
          tabBtns.forEach((b) => {
            const active = b === btn;
            b.classList.toggle('is-active', active);
            b.setAttribute('aria-selected', String(active));
          });
          panels.forEach((p) => {
            p.classList.toggle('is-active', p.id === 'tab-' + key);
          });
        });
      });
    });
  }

  function bindValidation() {
    document.querySelectorAll('form').forEach((form) => {
      if (form.classList.contains('footer__newsletter')) return; // handled in main.js
      form.addEventListener('submit', (e) => {
        let valid = true;
        form.querySelectorAll('[required]').forEach((input) => {
          const field = input.closest('.field');
          if (!field) return;
          const v = (input.value || '').trim();
          let ok = v.length > 0;
          if (ok && input.type === 'email') ok = /^\S+@\S+\.\S+$/.test(v);
          if (ok && input.type === 'tel')   ok = v.replace(/\D/g, '').length >= 7;
          field.classList.toggle('has-error', !ok);
          if (!ok) valid = false;
        });
        if (!valid) {
          e.preventDefault();
          const firstErr = form.querySelector('.field.has-error input, .field.has-error textarea, .field.has-error select');
          if (firstErr) firstErr.focus();
        }
      });

      // Clear error on input
      form.querySelectorAll('input, textarea, select').forEach((input) => {
        input.addEventListener('input', () => {
          const field = input.closest('.field');
          if (field) field.classList.remove('has-error');
        });
      });
    });
  }
})();
