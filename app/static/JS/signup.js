function handleSignup(e) {
    e.preventDefault();
  
    const email = document.querySelector('input[type="email"]').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
  
    // Check email format
    if (!isValidEmail(email)) {
      alert("Please enter a valid email address!");
      return;
    }
  
    // Check password strength
    if (!isPasswordSecure(password)) {
      alert("Password must meet all security rules.");
      return;
    }
  
    // Check password confirmation
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
  
    alert("Signup successful! (backend connection needed)");
  }
  
  // ✅ Password strength checker
  function isPasswordSecure(password) {
    const rules = [
      { regex: /.{8,}/, elementId: 'length-rule' },
      { regex: /[0-9]/, elementId: 'number-rule' },
      { regex: /[A-Z]/, elementId: 'uppercase-rule' },
      { regex: /[!@#$%^&*(),.?\":{}|<>]/, elementId: 'special-rule' },
    ];
  
    let allValid = true;
    rules.forEach(rule => {
      const element = document.getElementById(rule.elementId);
      if (rule.regex.test(password)) {
        element.classList.add('valid');
        element.classList.remove('invalid');
        element.innerText = "✔️ " + element.innerText.substring(2);
      } else {
        element.classList.add('invalid');
        element.classList.remove('valid');
        element.innerText = "❌ " + element.innerText.substring(2);
        allValid = false;
      }
    });
  
    return allValid;
  }
  
  // ✅ Email format checker
  function isValidEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/
    // This regex checks for a valid email format;
    return emailPattern.test(email);
  }
  
  // ✅ Toggle password visibility
  function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
      input.type = "text";
    } else {
      input.type = "password";
    }
  }
  
  // ✅ Setup live password checking on typing
  document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    passwordInput.addEventListener('input', function() {
      isPasswordSecure(passwordInput.value);
    });
  });
  