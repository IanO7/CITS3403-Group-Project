document.addEventListener('DOMContentLoaded', function () {
  // DOM Elements
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirm_password');
  const signupBtn = document.getElementById('signupBtn');
  const togglePassword = document.getElementById('toggle-password');
  const eyeIcon = document.getElementById('eye-icon');
  const toggleConfirmPassword = document.getElementById('toggle-confirm-password');
  const eyeIconConfirm = document.getElementById('eye-icon-confirm');

  // Password Validation Rules
  const rules = [
    { id: 'length-rule', regex: /.{8,}/, label: "At least 8 characters" },
    { id: 'number-rule', regex: /\d/, label: "At least one number (0-9)" },
    { id: 'uppercase-rule', regex: /[A-Z]/, label: "At least one uppercase letter (A-Z)" },
    { id: 'special-rule', regex: /[^a-zA-Z0-9]/, label: "At least one special character (!@#$%)" }
  ];

  // Helper Function: Update Rule Display
  function updateRuleDisplay(rule, isValid) {
    const element = document.getElementById(rule.id);
    if (!element) return;

    element.classList.toggle('valid', isValid);
    element.classList.toggle('invalid', !isValid);
    element.innerHTML = isValid
      ? `✔️ ${rule.label}`
      : `❌ ${rule.label}`;
  }

  // Password Validation
  function validatePassword() {
    const val = password.value;
    const confirmVal = confirmPassword.value;
    let allValid = true;

    // Validate password rules
    rules.forEach(rule => {
      const isValid = rule.regex.test(val);
      updateRuleDisplay(rule, isValid);
      if (!isValid) allValid = false;
    });

    // Validate password match
    const match = val === confirmVal && val !== "";
    updateRuleDisplay({ id: 'match-rule', label: "Both passwords must be the same" }, match);
    allValid = allValid && match;

    // Enable or disable the signup button
    signupBtn.disabled = !allValid;
  }

  // Event Listeners for Password Validation
  if (password) password.addEventListener('input', validatePassword);
  if (confirmPassword) confirmPassword.addEventListener('input', validatePassword);

  // Password Eye Toggle for Password
  let visible = false;
  if (password && togglePassword) {
    togglePassword.addEventListener('mousedown', function (e) {
      e.preventDefault(); // Prevents focus loss
    });
    togglePassword.addEventListener('click', function (e) {
      visible = !visible;
      password.type = visible ? 'text' : 'password';
      eyeIcon.innerHTML = visible
        ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
        : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
      password.focus(); // Keep focus on input
    });
  }

  // Password Eye Toggle for Confirm Password
  let visibleConfirm = false;
  if (confirmPassword && toggleConfirmPassword) {
    toggleConfirmPassword.addEventListener('mousedown', function (e) {
      e.preventDefault();
    });
    toggleConfirmPassword.addEventListener('click', function (e) {
      visibleConfirm = !visibleConfirm;
      confirmPassword.type = visibleConfirm ? 'text' : 'password';
      eyeIconConfirm.innerHTML = visibleConfirm
        ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
        : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
      confirmPassword.focus();
    });
  }

  // Final Check on Form Submission
  const form = document.querySelector('.signup-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      validatePassword(); // Ensure the latest state

      if (signupBtn.disabled) {
        e.preventDefault();
        alert("Please correct the highlighted issues before signing up.");
      }
    });
  }
});