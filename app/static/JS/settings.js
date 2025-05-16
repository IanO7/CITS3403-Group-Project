// Read CSRF token once
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute('content');

// Helper to POST a form via AJAX, using getAttribute to avoid name shadowing
function ajaxPost(form) {
  const url = form.getAttribute('action');
  const formData = new FormData(form);
  return fetch(url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken },
    body: formData
  }).then(r => r.json());
}

// Username validation
const usernameForm = document.getElementById('update-username-form');
usernameForm?.addEventListener('submit', function(event) {
  const username = document.getElementById('username').value.trim();
  if (username.length < 3) {
    event.preventDefault();
    showOzfoodyNotification('Username must be at least 3 characters long.', 'error');
  }
});

// Email validation
const emailForm = document.getElementById('update-email-form');
emailForm?.addEventListener('submit', function(event) {
  const email = document.getElementById('email').value.trim();
  if (!email.includes('@')) {
    event.preventDefault();
    showOzfoodyNotification("Please include an '@' in the email address.", 'error');
  }
});

// Extra confirmation for delete account
const deleteForm = document.getElementById('delete-account-form');
deleteForm?.addEventListener('submit', function(event) {
  event.preventDefault();
  showOzfoodyNotification(
    `Are you sure you want to delete your account? This action cannot be undone.<br>
     <button id="confirm-delete-btn" class="btn btn-danger mt-3 me-2">Yes, delete my account</button>
     <button id="cancel-delete-btn" class="btn btn-secondary mt-3">No, keep my account</button>`,
    'error',
    10000
  );

  setTimeout(() => {
    const yesBtn = document.getElementById('confirm-delete-btn');
    const noBtn = document.getElementById('cancel-delete-btn');

    yesBtn?.addEventListener('click', () => {
      ajaxPost(deleteForm)
        .then(data => {
          if (data.success) {
            showOzfoodyNotification(data.message, 'success');
            window.location.href = '/landing';
          } else {
            showOzfoodyNotification(data.error || 'An unexpected error occurred.', 'error');
          }
        })
        .catch(err => {
          showOzfoodyNotification('A network error occurred.', 'error');
          console.error('Fetch error:', err);
        });
    });

    noBtn?.addEventListener('click', () => {
      const notif = document.getElementById('ozfoody-notification');
      notif.classList.remove('show');
      setTimeout(() => { notif.style.display = 'none'; }, 300);
    });
  }, 100);
});

// Attach AJAX to all other forms
document.querySelectorAll('form').forEach(form => {
  if (form.id === 'delete-account-form') return;
  if (!form.id) return;
  form.addEventListener('submit', function(event) {
    // skip invalid
    if (!form.checkValidity()) return;
    event.preventDefault();
    ajaxPost(form)
      .then(data => {
        if (data.success) showOzfoodyNotification(data.message, 'success');
        else showOzfoodyNotification(data.error || 'An unexpected error occurred.', 'error');
      })
      .catch(err => {
        showOzfoodyNotification('A network error occurred.', 'error');
        console.error('Fetch error:', err);
      });
  });
});

// Password validation and toggles (unchanged)
document.addEventListener('DOMContentLoaded', function () {
  const elements = {
    newPassword: document.getElementById('new-password'),
    confirmPassword: document.getElementById('confirm-password'),
    updateBtn: document.getElementById('updateBtn'),
    toggleNewPassword: document.getElementById('toggle-new-password'),
    toggleConfirmPassword: document.getElementById('toggle-confirm-password'),
    eyeIconNew: document.getElementById('eye-icon-new'),
    eyeIconConfirm: document.getElementById('eye-icon-confirm')
  };

  if (!elements.newPassword || !elements.confirmPassword) return;

  const rules = [
    { id: 'length-rule', regex: /^.{8,128}$/, label: "8-128 characters" },
    { id: 'number-rule', regex: /\d/, label: "At least one number (0-9)" },
    { id: 'uppercase-rule', regex: /[A-Z]/, label: "At least one uppercase letter" },
    { id: 'special-rule', regex: /[^a-zA-Z0-9]/, label: "At least one special character" }
  ];

  function updateRuleDisplay(rule, isValid) {
    const el = document.getElementById(rule.id);
    if (!el) return;
    el.classList.toggle('valid', isValid);
    el.classList.toggle('invalid', !isValid);
    el.textContent = `${isValid ? '✔️' : '❌'} ${rule.label}`;
  }

  function checkPasswordRules() {
    let allValid = true;
    rules.forEach(rule => {
      const valid = rule.regex.test(elements.newPassword.value);
      updateRuleDisplay(rule, valid);
      if (!valid) allValid = false;
    });
    return allValid;
  }

  function checkPasswordsMatch() {
    const match = elements.newPassword.value === elements.confirmPassword.value;
    updateRuleDisplay({ id: 'match-rule', label: "Passwords match" }, match);
    return match;
  }

  function validatePassword() {
    const valid = checkPasswordRules() && checkPasswordsMatch();
    if (elements.updateBtn) {
      elements.updateBtn.disabled = !valid;
      elements.updateBtn.classList.toggle('btn-success', valid);
      elements.updateBtn.classList.toggle('btn-warning', !valid);
    }
  }

  [elements.newPassword, elements.confirmPassword].forEach(el => el.addEventListener('input', validatePassword));
  validatePassword();

  function toggleVisibility(input, toggle, icon) {
    let visible = false;
    toggle?.addEventListener('mousedown', e => e.preventDefault());
    toggle?.addEventListener('click', () => {
      visible = !visible;
      input.type = visible ? 'text' : 'password';
      icon.innerHTML = visible
        ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
        : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
    });
  }

  toggleVisibility(elements.newPassword, elements.toggleNewPassword, elements.eyeIconNew);
  toggleVisibility(elements.confirmPassword, elements.toggleConfirmPassword, elements.eyeIconConfirm);
});
