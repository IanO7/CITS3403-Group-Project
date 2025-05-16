// ─────────────────────────────────────────────────────────────────────────────
// 0. Pull CSRF token from meta into a global
// ─────────────────────────────────────────────────────────────────────────────
window.CSRF_TOKEN = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute('content');



// ─────────────────────────────────────────────────────────────────────────────
// 1. When DOM is ready, bind everything
// ─────────────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Comments
  document.querySelectorAll('.comment-button').forEach(btn => {
    btn.addEventListener('click', () => {
      const reviewId = btn.dataset.commentId;
      renderComments(reviewId);
    });
  });

  // Share (stub)
  document.querySelectorAll('.share-button').forEach(btn => {
    btn.addEventListener('click', handleShare);
  });

  // Delete (stub)
  document.querySelectorAll('.delete-button').forEach(btn => {
    btn.addEventListener('click', handleDelete);
  });

  // Like
  document.querySelectorAll('.like-button').forEach(btn => {
    btn.addEventListener('click', handleLike);
  });
});



// ─────────────────────────────────────────────────────────────────────────────
// 2. Render comments (unchanged)
// ─────────────────────────────────────────────────────────────────────────────
function renderComments(reviewId) {
  // Get current user ID from the main comment form in the modal
  const currentUserId = document.querySelector(`#commentsModal-${reviewId} input[name="user_id"]`).value;
  const comments = window[`comments_${reviewId}`] || [];
  const container = document.getElementById(`comment-area-${reviewId}`);
  container.innerHTML = '';

  comments.forEach(comment => {
    const wrapper = document.createElement('div');
    wrapper.id = `comment-${comment.id}`;
    wrapper.className = 'p-3 border rounded bg-light shadow-sm';
    wrapper.innerHTML = `
      <div>
        <img src="${comment.profileImage}" class="profileImageSmaller" alt="profile pic"/>
        <strong>${comment.username}</strong>
      </div>
      <p>${comment.Comment}</p>
      <button class="btn btn-sm btn-outline-primary reply-toggle" data-id="${comment.id}">Reply</button>
      <div id="reply-form-${comment.id}" class="d-none">
        <form method="POST">
          <input type="hidden" name="csrf_token" value="${window.CSRF_TOKEN}" />
          <input type="hidden" name="note_id" value="${reviewId}" />
          <input type="hidden" name="parentID" value="${comment.id}" />
          **<input type="hidden" name="user_id" value="${currentUserId}" />**
          <textarea name="Comment" class="form-control mb-2" required></textarea>
          <button type="submit" class="btn btn-primary btn-sm">Reply</button>
        </form>
      </div>
    `;
    container.appendChild(wrapper);
  });

 



  // Toggle reply forms
  container.querySelectorAll('.reply-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      document.getElementById(`reply-form-${id}`).classList.toggle('d-none');
    });
  });
}






// ─────────────────────────────────────────────────────────────────────────────
// 4. Like handler: no JSON header & valid CSRF
// ─────────────────────────────────────────────────────────────────────────────
function handleLike(evt) {
  const btn = evt.currentTarget;
  const noteId = btn.dataset.noteId;

  fetch(`/like/${noteId}`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': window.CSRF_TOKEN
    }
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      btn.querySelector('.action-count').textContent = data.likes;
    } else {
      console.error('Like failed:', data.error);
    }
  })
  .catch(err => console.error('Network error:', err));
}
