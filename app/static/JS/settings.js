//keep code from here
// Username validation
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute('content');
document.getElementById('update-username-form').addEventListener('submit', function(event) {
    
    const username = document.getElementById('username').value.trim();
    if (username.length < 3) {
        showOzfoodyNotification("Username must be at least 3 characters long.", "error");
        event.preventDefault();
        return false;
    }
});

// Email validation
document.getElementById('update-email-form').addEventListener('submit', function(event) {
    const email = document.getElementById('email').value.trim();
    if (!email.includes('@')) {
        showOzfoodyNotification("Please include an '@' in the email address.", "error");
        event.preventDefault();
        return false;
    }
});

// Extra confirmation for delete account
document.getElementById('delete-account-form').addEventListener('submit', function(event) {
    event.preventDefault();
    showOzfoodyNotification(
        `Are you sure you want to delete your account? This action cannot be undone.<br>
        <button id="confirm-delete-btn" class="btn btn-danger mt-3 me-2">Yes, delete my account</button>
        <button id="cancel-delete-btn" class="btn btn-secondary mt-3">No, keep my account</button>`,
        "error",
        10000
    );
    setTimeout(() => {
        const yesBtn = document.getElementById('confirm-delete-btn');
        const noBtn = document.getElementById('cancel-delete-btn');

        if (yesBtn) {
            yesBtn.onclick = function(e) {
                // Ensure the action field is present
                const form = document.getElementById('delete-account-form');
                let actionInput = form.querySelector('input[name="action"]');
                if (!actionInput) {
                    actionInput = document.createElement('input');
                    actionInput.type = 'hidden';
                    actionInput.name = 'action';
                    actionInput.value = 'delete_account';
                    form.appendChild(actionInput);
                }
                // Submit via fetch
                const formData = new FormData(form);
fetch('/settings', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken
    },
    body: formData
})
                .then(r => r.json())
                .then(data => {we
                    if (data.success) {
                        showOzfoodyNotification(data.message, "success");
                        window.location.href = '/landing';
                    } else {
                        showOzfoodyNotification(data.error || 'An unexpected error occurred.', "error");
                    }
                })
                .catch(err => {
                    showOzfoodyNotification('A network error occurred.', "error");
                    console.error('Fetch error:', err);
                });
            };
        }

        if (noBtn) {
            noBtn.onclick = function(e) {
                const notif = document.getElementById("ozfoody-notification");
                notif.classList.remove("show");
                setTimeout(() => { notif.style.display = "none"; }, 300);
            };
        }
    }, 100);
});

// Attach enhanced fetch handling to all forms except delete-account-form
document.querySelectorAll('form').forEach(form => {
    if (form.id === 'delete-account-form') return;
    form.addEventListener('submit', event => {
        if (!form.checkValidity()) return;
        event.preventDefault();
        const formData = new FormData(form, event.submitter);
fetch('/settings', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: formData
})
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                showOzfoodyNotification(data.message, "success");
            } else {
                showOzfoodyNotification(data.error || 'An unexpected error occurred.', "error");
            }
        })
        .catch(err => {
            showOzfoodyNotification('A network error occurred.', "error");
            console.error('Fetch error:', err);
        });
    });
});


// Password validation setup
document.addEventListener('DOMContentLoaded', function () {
    // Get DOM elements
    const elements = {
        newPassword: document.getElementById('new-password'),
        confirmPassword: document.getElementById('confirm-password'),
        updateBtn: document.getElementById('updateBtn'),
        toggleNewPassword: document.getElementById('toggle-new-password'),
        toggleConfirmPassword: document.getElementById('toggle-confirm-password'),
        eyeIconNew: document.getElementById('eye-icon-new'),
        eyeIconConfirm: document.getElementById('eye-icon-confirm')
    };

    // Check if password elements exist
    if (!elements.newPassword || !elements.confirmPassword) {
        console.warn('Password form elements not found');
        return;
    }

    // Password validation rules
    const rules = [
        { id: 'length-rule', regex: /^.{8,128}$/, label: "8-128 characters" },
        { id: 'number-rule', regex: /\d/, label: "At least one number (0-9)" },
        { id: 'uppercase-rule', regex: /[A-Z]/, label: "At least one uppercase letter" },
        { id: 'special-rule', regex: /[^a-zA-Z0-9]/, label: "At least one special character" }
    ];

    // Password validation helpers remain the same
    function updateRuleDisplay(rule, isValid) {
        const element = document.getElementById(rule.id);
        if (!element) return;
        
        element.classList.toggle('valid', isValid);
        element.classList.toggle('invalid', !isValid);
        element.innerHTML = `${isValid ? '✔️' : '❌'} ${rule.label}`;
    }

    function checkPasswordRules() {
        if (!elements.newPassword?.value) return false;
        
        let allValid = true;
        rules.forEach(rule => {
            const isValid = rule.regex.test(elements.newPassword.value);
            updateRuleDisplay(rule, isValid);
            if (!isValid) allValid = false;
        });
        return allValid;
    }

    function checkPasswordsMatch() {
        if (!elements.newPassword?.value || !elements.confirmPassword?.value) return false;
        const match = elements.newPassword.value === elements.confirmPassword.value;
        updateRuleDisplay({ id: 'match-rule', label: "Passwords match" }, match);
        return match;
    }

    // Simplified password validation
    function validatePassword() {
        const rulesValid = checkPasswordRules();
        const matchValid = checkPasswordsMatch();

        const isValid = rulesValid && matchValid;
        if (elements.updateBtn) {
            elements.updateBtn.disabled = !isValid;
            elements.updateBtn.classList.toggle('btn-success', isValid);
            elements.updateBtn.classList.toggle('btn-warning', !isValid);
        }
    }

    // Add event listeners
    [elements.newPassword, elements.confirmPassword].forEach(element => {
        element?.addEventListener('input', validatePassword);
    });

    // Initialize password validation
    validatePassword();

    // Password visibility toggles
    function createEyeToggle(input, toggle, icon) {
        let visible = false;
        if (!input || !toggle || !icon) return;

        toggle.addEventListener('mousedown', e => e.preventDefault());
        toggle.addEventListener('click', () => {
            visible = !visible;
            input.type = visible ? 'text' : 'password';
            icon.innerHTML = visible
                ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
                : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
            input.focus();
        });
    }

    // Initialize password toggles (removed current password toggle)
    createEyeToggle(elements.newPassword, elements.toggleNewPassword, elements.eyeIconNew);
    createEyeToggle(elements.confirmPassword, elements.toggleConfirmPassword, elements.eyeIconConfirm);
});
