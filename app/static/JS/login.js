// File: static/js/login.js

// Function to hadle login with Google
function handleGoogleLogin() {
  alert("Redirecting to Google login...");
}

// Function to check if the email is valid
function isValidEmail(email) {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
}

// Hide error when email input is focused
document.addEventListener('DOMContentLoaded', function() {
  const emailInput = document.getElementById('email-input');
  const errorDiv = document.getElementById('login-error');

  if (emailInput && errorDiv) {
    emailInput.addEventListener('blur', function() {
      if (!isValidEmail(emailInput.value)) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Please enter a valid email address.';
      } else {
        errorDiv.style.display = 'none';
      }
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
