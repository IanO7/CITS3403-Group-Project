document.addEventListener('DOMContentLoaded', () => {
  // Attach click handlers to all comment buttons
  document.querySelectorAll('.comment-button').forEach(button => {
    button.addEventListener('click', () => {
      const reviewId = button.dataset.commentId;
      renderComments(reviewId);
    });
  });

  // Attach click handlers for share, delete, like as needed
  document.querySelectorAll('.share-button').forEach(btn => {
    btn.addEventListener('click', handleShare);
  });
  document.querySelectorAll('.delete-button').forEach(btn => {
    btn.addEventListener('click', handleDelete);
  });
  document.querySelectorAll('.like-button').forEach(btn => {
    btn.addEventListener('click', handleLike);
  });
});

/**
 * Fetches and renders comments for a given review inside its modal.
 * Assumes a global comments_<id> variable is injected for initial data.
 */
function renderComments(reviewId) {
  const comments = window[`comments_${reviewId}`] || [];
  const container = document.getElementById(`comment-area-${reviewId}`);
  container.innerHTML = '';

  comments.forEach(comment => {
    const wrapper = document.createElement('div');
    wrapper.id = `comment-${comment.id}`;
    wrapper.className = 'p-3 border rounded bg-light shadow-sm';
    wrapper.innerHTML = `
      <div>
        <img src="${comment.profileImage}" class="profileImageSmaller" />
        <strong>${comment.username}</strong>
      </div>
      <p>${comment.Comment}</p>
      <button class="btn btn-sm btn-outline-primary reply-toggle" data-id="${comment.id}">Reply</button>
      <div id="reply-form-${comment.id}" class="d-none">
        <form method="POST">
          <input type="hidden" name="csrf_token" value="${window.CSRF_TOKEN}" />
          <input type="hidden" name="note_id" value="${reviewId}" />
          <input type="hidden" name="parentID" value="${comment.id}" />
          <textarea name="Comment" class="form-control mb-2" required></textarea>
          <button type="submit" class="btn btn-primary btn-sm">Reply</button>
        </form>
      </div>
    `;
    container.appendChild(wrapper);
  });

  // Attach reply-toggle toggles
  container.querySelectorAll('.reply-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      document.getElementById(`reply-form-${id}`).classList.toggle('d-none');
    });
  });
}

function handleShare(evt) {
  const noteId = evt.currentTarget.dataset.noteId;
  // implement share logic here
}

function handleDelete(evt) {
  const noteId = evt.currentTarget.dataset.noteId;
  // implement delete logic here
}

function handleLike(evt) {
  const noteId = evt.currentTarget.dataset.noteId;
  const csrf = window.CSRF_TOKEN;
  fetch(`/like/${noteId}`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrf }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const countEl = evt.currentTarget.querySelector('.action-count');
      countEl.textContent = data.likes;
    }
  });
}
