// File: static/js/login.js

function handleGoogleLogin() {
  alert("Redirecting to Google login...");
}

// Hide error when email input is focused
document.addEventListener('DOMContentLoaded', function() {
  var emailInput = document.getElementById('email-input');
  var errorDiv = document.getElementById('login-error');
  if(emailInput && errorDiv) {
    emailInput.addEventListener('focus', function() {
      errorDiv.style.display = 'none';
    });
  }

  // Password eye toggle
  var passwordInput = document.getElementById('password-input');
  var togglePassword = document.getElementById('toggle-password');
  var eyeIcon = document.getElementById('eye-icon');
  let visible = false;
  if(passwordInput && togglePassword && eyeIcon) {
    togglePassword.addEventListener('click', function() {
      visible = !visible;
      passwordInput.type = visible ? 'text' : 'password';
      // Toggle a CSS class for the SVG to show/hide the "slash"
      eyeIcon.classList.toggle('eye-off', visible);
    });
  }
});
