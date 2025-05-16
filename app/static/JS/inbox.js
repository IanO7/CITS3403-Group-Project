document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.approve-follow-btn').forEach(btn => {
        btn.addEventListener('click', function() {
    fetch(`/approve_follow/${btn.dataset.id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
        .then(res => res.json())
        .then(data => {
            showOzfoodyNotification(data.message || "Request approved.", "success");
            btn.closest('li').remove();
        });
        });
    });
    document.querySelectorAll('.reject-follow-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        fetch(`/reject_follow/${btn.dataset.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(res => res.json())
        .then(data => {
            showOzfoodyNotification(data.message || "Request rejected.", "error");
            btn.closest('li').remove();
        });
    });
    });
});