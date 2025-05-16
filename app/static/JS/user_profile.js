document.addEventListener('DOMContentLoaded', () => {
  const followAction = document.getElementById('follow-action');
  if (!followAction) return;

  const followUrl   = followAction.dataset.followUrl;
  const unfollowUrl = followAction.dataset.unfollowUrl;
  const approveUrl  = followAction.dataset.approveUrl;
  const rejectUrl   = followAction.dataset.rejectUrl;
  const csrfToken   = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  const doPost = (url, onSuccessHtml, defaultMsg) => {
    fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken }
    })
    .then(r => r.json())
    .then(data => {
      showOzfoodyNotification(data.message || data.error || defaultMsg,
                              data.success ? 'success' : 'error');
      if (data.success) followAction.innerHTML = onSuccessHtml;
    })
    .catch(err => { console.error(err); showOzfoodyNotification('Error','error'); });
  };

  followAction.addEventListener('click', e => {
    switch (e.target.id) {
      case 'follow-btn':
        doPost(followUrl,
               '<button class="btn btn-secondary" disabled>Request Sent</button>',
               'Request sent.');
        break;
      case 'unfollow-btn':
        doPost(unfollowUrl,
               '<button class="btn btn-primary" id="follow-btn">Send Follow Request</button>',
               'Unfollowed.');
        break;
      case 'approve-btn':
        // Use approveUrl directly (already contains the ID)
        doPost(approveUrl,
               '<button class="btn btn-success" id="unfollow-btn">Following</button>',
               'Approved.');
        break;
      case 'reject-btn':
        // Use rejectUrl directly (already contains the ID)
        doPost(rejectUrl,
               '<button class="btn btn-primary" id="follow-btn">Send Follow Request</button>',
               'Rejected.');
        break;
      default:
        return;
    }
  });
});