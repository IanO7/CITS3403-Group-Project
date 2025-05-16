document.addEventListener('DOMContentLoaded', () => {
  // 1. Pull CSRF token from the meta tag
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content');

  // 2. Multi-share toggle
  document.getElementById('shareMultipleBtn').addEventListener('click', () => {
    document.getElementById('Posts').classList.add('multi-share-mode');
    document.getElementById('shareSelectedBtn').classList.remove('d-none');
  });

  document.getElementById('shareSelectedBtn').addEventListener('click', () => {
    const checked = document.querySelectorAll('.multi-share-checkbox:checked');
    if (!checked.length) {
      const alertDiv = document.getElementById('multiShareAlert');
      alertDiv.className = 'alert alert-danger';
      alertDiv.textContent = 'Please select at least one post to share.';
      alertDiv.classList.remove('d-none');
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
      return;
    }
    // open multi-share modal
    new bootstrap.Modal(document.getElementById('multiShareModal')).show();
  });

  // 3. Like buttons
  document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
      const noteId = button.dataset.noteId;
      fetch(`/like/${noteId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          button.querySelector('.action-count').textContent = data.likes;
        } else {
          console.error(data.error);
        }
      })
      .catch(err => console.error('Error:', err));
    });
  });

  // 4. Delete post
  let postToDeleteId = null;
  document.querySelectorAll('.delete-button').forEach(btn => {
    btn.addEventListener('click', () => {
      postToDeleteId = btn.dataset.noteId;
      new bootstrap.Modal(document.getElementById('deletePostModal')).show();
    });
  });

  document.getElementById('confirmDeletePostBtn').addEventListener('click', () => {
    if (!postToDeleteId) return;
    fetch(`/delete_post/${postToDeleteId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    })
    .then(response => {
      const alertDiv = document.getElementById('singleShareAlert');
      if (response.ok) {
        alertDiv.className = 'alert alert-success';
        alertDiv.textContent = 'Post deleted successfully!';
        alertDiv.classList.remove('d-none');
        setTimeout(() => location.reload(), 1500);
      } else {
        alertDiv.className = 'alert alert-danger';
        alertDiv.textContent = 'Failed to delete the post.';
        alertDiv.classList.remove('d-none');
        setTimeout(() => alertDiv.classList.add('d-none'), 4000);
      }
    })
    .catch(() => {
      const alertDiv = document.getElementById('singleShareAlert');
      alertDiv.className = 'alert alert-danger';
      alertDiv.textContent = 'Failed to delete the post.';
      alertDiv.classList.remove('d-none');
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
    })
    .finally(() => {
      bootstrap.Modal.getInstance(document.getElementById('deletePostModal')).hide();
      postToDeleteId = null;
    });
  });

  // 5. Single-share modal
  let shareNoteId = null;
  document.querySelectorAll('.share-button').forEach(btn => {
    btn.addEventListener('click', () => {
      shareNoteId = btn.dataset.noteId;
      new bootstrap.Modal(document.getElementById('shareModal')).show();
    });
  });

  document.getElementById('recipientSearch').addEventListener('input', function() {
    const q = this.value.trim();
    const results = document.getElementById('userResults');
    results.innerHTML = '';
    if (!q) return;
    fetch(`/api/users?q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(data => {
        data.users.forEach(u => {
          const item = document.createElement('button');
          item.type = 'button';
          item.className = 'list-group-item list-group-item-action';
          item.textContent = u.username;
          item.onclick = () => {
            this.value = u.username;
            results.innerHTML = '';
            this.selectedUserId = u.id;
          };
          results.appendChild(item);
        });
      });
  });

  document.getElementById('confirmShareBtn').addEventListener('click', () => {
    const userId = document.getElementById('recipientSearch').selectedUserId;
    if (!userId) {
      const alertDiv = document.getElementById('singleShareAlert');
      alertDiv.className = 'alert alert-danger';
      alertDiv.textContent = 'Please select a user to share with.';
      alertDiv.classList.remove('d-none');
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
      return;
    }
    fetch('/share_post', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ note_id: shareNoteId, recipient_id: userId })
    })
    .then(r => r.json())
    .then(data => {
      const alertDiv = document.getElementById('singleShareAlert');
      if (data.success) {
        alertDiv.className = 'alert alert-success';
        alertDiv.innerHTML = `<strong>Success!</strong> ${data.message || 'Post shared!'}`;
        alertDiv.classList.remove('d-none');
        bootstrap.Modal.getInstance(document.getElementById('shareModal')).hide();
      } else {
        alertDiv.className = 'alert alert-danger';
        alertDiv.textContent = data.error || 'Failed to share';
        alertDiv.classList.remove('d-none');
      }
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
    })
    .catch(() => {
      const alertDiv = document.getElementById('singleShareAlert');
      alertDiv.className = 'alert alert-danger';
      alertDiv.textContent = 'Failed to share';
      alertDiv.classList.remove('d-none');
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
    });
  });

  // 6. Multi-share modal
  document.getElementById('confirmMultiShareBtn').addEventListener('click', () => {
    const selectedUserId = document.getElementById('multiRecipientSearch').selectedUserId;
    const noteIds = Array.from(document.querySelectorAll('.multi-share-checkbox:checked'))
                      .map(cb => cb.value);
    if (!selectedUserId || !noteIds.length) {
      const alertDiv = document.getElementById('multiShareAlert');
      alertDiv.className = 'alert alert-danger';
      alertDiv.textContent = !selectedUserId
        ? 'Please select a user to share with.'
        : 'Please select at least one post to share.';
      alertDiv.classList.remove('d-none');
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
      return;
    }
    fetch('/share_multiple_posts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ note_ids: noteIds, recipient_id: selectedUserId })
    })
    .then(r => r.json())
    .then(data => {
      const alertDiv = document.getElementById('multiShareAlert');
      if (data.success) {
        alertDiv.className = 'alert alert-success';
        alertDiv.innerHTML = `
          <strong>Success!</strong> ${data.shared} post(s) shared.
          ${data.ignored ? data.ignored + ' ignored.' : ''}
        `;
        alertDiv.classList.remove('d-none');
        bootstrap.Modal.getInstance(document.getElementById('multiShareModal')).hide();
      } else {
        alertDiv.className = 'alert alert-danger';
        alertDiv.textContent = data.error || 'Failed to share';
        alertDiv.classList.remove('d-none');
      }
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
    })
    .catch(() => {
      const alertDiv = document.getElementById('multiShareAlert');
      alertDiv.className = 'alert alert-danger';
      alertDiv.textContent = 'Failed to share';
      alertDiv.classList.remove('d-none');
      setTimeout(() => alertDiv.classList.add('d-none'), 4000);
    });
  });
});
