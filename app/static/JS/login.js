// File: static/js/login.js
<<<<<<< HEAD
function handleGoogleLogin() {
    alert("Redirect to Google login (OAuth setup needed in backend)");
  }
  
  function handleEmailLogin(e) {
    e.preventDefault();
    alert("Handle email login (to be implemented with Flask backend)");
  }
=======

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
  if(passwordInput && togglePassword) {
    togglePassword.addEventListener('click', function() {
      visible = !visible;
      passwordInput.type = visible ? 'text' : 'password';
      // Change icon (simple swap between eye and eye-off)
      eyeIcon.innerHTML = visible
        ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
        : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
    });
  }
});
>>>>>>> 883a95fa7da8a491448ff0d6ee8289c5dbc0b95f
  