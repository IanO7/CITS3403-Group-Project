document.addEventListener('DOMContentLoaded', function() {
  // Pull the CSRF token from the <meta> tag
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  const followAction = document.getElementById('follow-action');
  if (!followAction) return;

  followAction.addEventListener('click', function(e) {
    // Helper to POST JSON and handle the response
    const doPost = (url, onSuccessHtml, defaultMsg) => {
      fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          }
        })
        .then(res => res.json())
        .then(data => {
          showOzfoodyNotification(
            data.message || data.error || defaultMsg,
            data.success ? 'success' : 'error'
          );
          if (data.success) {
            followAction.innerHTML = onSuccessHtml;
          }
        })
        .catch(err => {
          console.error(err);
          showOzfoodyNotification('An error occurred', 'error');
        });
    };

    // Send follow request
    if (e.target.id === 'follow-btn') {
      doPost(
        '{{ url_for("views.follow", user_id=selected_user.id) }}',
        '<button class="btn btn-secondary" disabled>Request Sent</button>',
        'Request sent.'
      );
    }

    // Unfollow
    else if (e.target.id === 'unfollow-btn') {
      doPost(
        '{{ url_for("views.unfollow", user_id=selected_user.id) }}',
        '<button class="btn btn-primary" id="follow-btn">Send Follow Request</button>',
        'Unfollowed.'
      );
    }

    // Approve
    else if (e.target.id === 'approve-btn') {
      const followId = e.target.getAttribute('data-id');
      doPost(
        `/approve_follow/${followId}`,
        '<button class="btn btn-success" id="unfollow-btn">Following</button>',
        'Approved.'
      );
    }

    // Reject
    else if (e.target.id === 'reject-btn') {
      const followId = e.target.getAttribute('data-id');
      doPost(
        `/reject_follow/${followId}`,
        '<button class="btn btn-primary" id="follow-btn">Send Follow Request</button>',
        'Rejected.'
      );
    }
  });
});
