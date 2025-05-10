// Password validation logic for both signup and settings pages

function updateCheck(element, isValid) {
  if (!element) return;
  element.className = isValid ? "valid" : "invalid";
  element.innerHTML = isValid
    ? element.innerHTML.replace('❌', '✔️')
    : element.innerHTML.replace('✔️', '❌');
}

// Generic password validation for any page
function validatePasswordFields(passwordId, confirmId, rules) {
  const password = document.getElementById(passwordId);
  const confirm = document.getElementById(confirmId);

  if (!password || !confirm) return;

  const val = password.value;
  const confirmVal = confirm.value;

  const hasLetter = /[a-zA-Z]/.test(val);
  const hasNumber = /\d/.test(val);
  const hasSymbol = /[^a-zA-Z0-9]/.test(val);
  const isLong = val.length >= 8;
  const isMatch = val === confirmVal && val !== "";

  updateCheck(document.getElementById(rules.length), isLong);
  updateCheck(document.getElementById(rules.letter), hasLetter);
  updateCheck(document.getElementById(rules.number), hasNumber);
  updateCheck(document.getElementById(rules.symbol), hasSymbol);
  updateCheck(document.getElementById(rules.match), isMatch);

  return isLong && hasLetter && hasNumber && hasSymbol && isMatch;
}

// Setup live validation for a form
function setupPasswordValidation(passwordId, confirmId, buttonId, rules) {
  const password = document.getElementById(passwordId);
  const confirm = document.getElementById(confirmId);
  const btn = document.getElementById(buttonId);

  function validate() {
    const valid = validatePasswordFields(passwordId, confirmId, rules);
    if (btn) btn.disabled = !valid;
  }

  if (password) password.addEventListener("input", validate);
  if (confirm) confirm.addEventListener("input", validate);
  // Initial state
  validate();
}

// Email format checker
function isValidEmail(email) {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
}

// Password eye toggle
function setupPasswordToggle(inputId, toggleId, iconId) {
  const input = document.getElementById(inputId);
  const toggle = document.getElementById(toggleId);
  const icon = document.getElementById(iconId);
  let visible = false;
  if (input && toggle && icon) {
    toggle.addEventListener('click', function() {
      visible = !visible;
      input.type = visible ? 'text' : 'password';
      icon.innerHTML = visible
        ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
        : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
    });
  }
}

// Notification display logic
function showOzfoodyNotification(message, type = "success", duration = 2500) {
  const notif = document.getElementById("ozfoody-notification");
  if (!notif) return;
  notif.textContent = message;
  notif.className = `ozfoody-notification show ${type}`;
  notif.style.display = "block";
  setTimeout(() => {
    notif.classList.remove("show");
    setTimeout(() => { notif.style.display = "none"; }, 300);
  }, duration);
}

// Export functions for use in HTML pages
window.OzfoodyPassword = {
  setupPasswordValidation,
  isValidEmail,
  setupPasswordToggle
};

// Export to window for use in inline scripts
window.showOzfoodyNotification = showOzfoodyNotification;
