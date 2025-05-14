document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements - Match HTML IDs exactly
    const currentPassword = document.getElementById('current-password');
    const newPassword = document.getElementById('new-password');
    const confirmPassword = document.getElementById('confirm-password');
    const updateBtn = document.getElementById('updateBtn');
    const togglePassword = document.getElementById('toggle-password');
    const toggleNewPassword = document.getElementById('toggle-new-password');
    const toggleConfirmPassword = document.getElementById('toggle-confirm-password');
    const eyeIcon = document.querySelector('#toggle-password svg');
    const eyeIconNew = document.querySelector('#toggle-new-password svg');
    const eyeIconConfirm = document.querySelector('#toggle-confirm-password svg');

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

        if (isValid) {
            element.classList.remove('invalid');
            element.classList.add('valid');
            element.innerHTML = `✔️ ${rule.label}`;
        } else {
            element.classList.remove('valid');
            element.classList.add('invalid');
            element.innerHTML = `❌ ${rule.label}`;
        }
    }

    // Add password verification
    async function verifyCurrentPassword() {
        const response = await fetch('/verify_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                current_password: currentPassword.value
            })
        });
        
        const data = await response.json();
        return data.valid;
    }

    // Password Validation
    async function validatePassword() {
        if (!newPassword || !confirmPassword || !currentPassword) return false;
        
        const val = newPassword.value;
        const confirmVal = confirmPassword.value;
        let allValid = true;

        // Validate each rule
        rules.forEach(rule => {
            const isValid = rule.regex.test(val);
            updateRuleDisplay(rule, isValid);
            if (!isValid) allValid = false;
        });

        // Check password match
        const match = val === confirmVal && val !== "";
        updateRuleDisplay({ id: 'match-rule', label: "Both passwords must be the same" }, match);
        allValid = allValid && match;

        // Verify current password
        if (currentPassword.value) {
            const isCurrentValid = await verifyCurrentPassword();
            updateRuleDisplay(
                { id: 'current-password-rule', label: "Current password is correct" },
                isCurrentValid
            );
            allValid = allValid && isCurrentValid;
        }

        // Enable/disable update button
        if (updateBtn) {
            updateBtn.disabled = !allValid;
        }

        return allValid;
    }

    // Event Listeners
    if (newPassword) {
        newPassword.addEventListener('input', validatePassword);
        newPassword.addEventListener('change', validatePassword);
    }
    
    if (confirmPassword) {
        confirmPassword.addEventListener('input', validatePassword);
        confirmPassword.addEventListener('change', validatePassword);
    }
    
    if (currentPassword) {
        currentPassword.addEventListener('input', validatePassword);
        currentPassword.addEventListener('change', validatePassword);
    }

    // Initial validation check
    validatePassword();

    // Password Eye Toggle for Current Password
    let visibleCurrent = false;
    if (currentPassword && togglePassword) {
        togglePassword.addEventListener('mousedown', function (e) {
            e.preventDefault(); // Prevents focus loss
        });
        togglePassword.addEventListener('click', function (e) {
            visibleCurrent = !visibleCurrent;
            currentPassword.type = visibleCurrent ? 'text' : 'password';
            eyeIcon.innerHTML = visibleCurrent
                ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
                : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
            currentPassword.focus(); // Keep focus on input
        });
    }

    // Password Eye Toggle for New Password
    let visibleNew = false;
    if (newPassword && toggleNewPassword) {
        toggleNewPassword.addEventListener('mousedown', function (e) {
            e.preventDefault(); // Prevents focus loss
        });
        toggleNewPassword.addEventListener('click', function (e) {
            visibleNew = !visibleNew;
            newPassword.type = visibleNew ? 'text' : 'password';
            eyeIconNew.innerHTML = visibleNew
                ? `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/><line x1="4" y1="20" x2="20" y2="4" stroke="#888" stroke-width="2"/>`
                : `<path stroke="#888" stroke-width="2" d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3.5" stroke="#888" stroke-width="2"/>`;
            newPassword.focus(); // Keep focus on input
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

            if (updateBtn.disabled) {
                e.preventDefault();
                alert("Please correct the highlighted issues before updating.");
            }
        });
    }

    // Add form submission handler
    document.getElementById('update-password-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate password first
        if (!await validatePassword()) {
            showOzfoodyNotification('Please fix validation errors first', 'error');
            return;
        }
        
        const formData = new FormData(this);
        formData.append('action', 'update_password');  // Add this line to specify the action
        
        try {
            const response = await fetch('/settings', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'  // Add this to maintain session
            });
            
            const data = await response.json();
            if (data.success) {
                showOzfoodyNotification('Password updated successfully', 'success');
                this.reset();
                // Reset validation states
                rules.forEach(rule => updateRuleDisplay(rule, false));
            } else {
                showOzfoodyNotification(data.error || 'Failed to update password', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showOzfoodyNotification('An error occurred while updating password', 'error');
        }
    });
});