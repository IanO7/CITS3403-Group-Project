
document.addEventListener('DOMContentLoaded', function() {
    const followAction = document.getElementById('follow-action');
    if (!followAction) return;

    // Read CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    followAction.addEventListener('click', function(e) {
        // Helper to send POST with CSRF
        function postAction(url) {
            return fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            }).then(res => res.json());
        }

        // Send Follow Request
        if (e.target && e.target.id === 'follow-btn') {
            postAction(followAction.getAttribute('data-follow-url'))
                .then(data => {
                    showOzfoodyNotification(data.message || data.error || 'Request sent.', data.success ? 'success' : 'error');
                    if (data.success) {
                        followAction.innerHTML = '<button class="btn btn-secondary" disabled>Request Sent</button>';
                    }
                });
        }
        // Unfollow
        if (e.target && e.target.id === 'unfollow-btn') {
            postAction(followAction.getAttribute('data-unfollow-url'))
                .then(data => {
                    showOzfoodyNotification(data.message || data.error || 'Unfollowed.', data.success ? 'success' : 'error');
                    if (data.success) {
                        followAction.innerHTML = '<button class="btn btn-primary" id="follow-btn">Send Follow Request</button>';
                    }
                });
        }
        // Approve
        if (e.target && e.target.id === 'approve-btn') {
            const followId = e.target.dataset.id;
            postAction(`/approve_follow/${followId}`)
                .then(data => {
                    showOzfoodyNotification(data.message || data.error || 'Approved.', data.success ? 'success' : 'error');
                    if (data.success) {
                        followAction.innerHTML = '<button class="btn btn-success" id="unfollow-btn">Following</button>';
                    }
                });
        }
        // Reject
        if (e.target && e.target.id === 'reject-btn') {
            const followId = e.target.dataset.id;
            postAction(`/reject_follow/${followId}`)
                .then(data => {
                    showOzfoodyNotification(data.message || data.error || 'Rejected.', data.success ? 'success' : 'error');
                    if (data.success) {
                        followAction.innerHTML = '<button class="btn btn-primary" id="follow-btn">Send Follow Request</button>';
                    }
                });
        }
    });
});
