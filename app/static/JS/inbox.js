document.addEventListener('DOMContentLoaded', function() {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  // Handle approve button clicks
  document.querySelectorAll('.approve-follow-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const requestItem = btn.closest('li');
      const approveUrl = requestItem.dataset.approveUrl;
      fetch(approveUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
      })
      .then(res => res.json())
      .then(data => {
        // Show success notification and remove the request from the list
        showOzfoodyNotification(data.message || "Follow request approved.", "success");
        requestItem.remove();
      });
    });
  });

  // Handle reject button clicks
  document.querySelectorAll('.reject-follow-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const requestItem = btn.closest('li');
      const rejectUrl = requestItem.dataset.rejectUrl;
      fetch(rejectUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
      })
      .then(res => res.json())
      .then(data => {
        // Show rejection notification and remove the request from the list
        showOzfoodyNotification(data.message || "Follow request rejected.", "error");
        requestItem.remove();
      });
    });
  });

  // Comment button logic starts here
  document.querySelectorAll('.comment-button').forEach(btn => {
    btn.addEventListener('click', () => {
      postIdInput.value = btn.dataset.postId;
      textInput.value = '';
      commentModal.show();
    });
  });

  // 2) Intercept form submit → AJAX POST
  form.addEventListener('submit', e => {
    e.preventDefault();
    const payload = {
      note_id: postIdInput.value,
      comment: textInput.value,
      parentID: 0
    };

    fetch('{{ url_for("views.post_comment") }}', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        commentModal.hide();
        // You can either:
        //  • append data.comment_html into the post’s comment list
        //  • or simply reload the page/that section
        location.reload();
      } else {
        alert(data.error || 'Failed to post comment');
      }
    })
    .catch(() => alert('Network error.'));
  });
});
