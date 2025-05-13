document.getElementById('shareMultipleBtn').addEventListener('click', function () {
    const checkboxes = document.querySelectorAll('.multi-share-checkbox');
    checkboxes.forEach(container => {
        container.style.display = container.style.display === 'none' ? 'block' : 'none';
    });
});

document.getElementById('shareSelectedBtn').addEventListener('click', function () {
    const checkboxes = document.querySelectorAll('.multi-share-checkbox');
    checkboxes.forEach(container => {
        container.style.display = container.style.display === 'none' ? 'block' : 'none';
    });
});

document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
        const noteId = button.getAttribute('data-note-id');
        fetch(`/like/${noteId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const likeCount = button.querySelector('.action-count');
                    likeCount.textContent = data.likes;
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    });
});

document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', () => {
        const noteId = button.getAttribute('data-note-id');
        if (confirm("Are you sure you want to delete this post?")) {
            fetch(`/delete_post/${noteId}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        alert("Post deleted successfully!");
                        location.reload();
                    } else {
                        alert("Failed to delete the post. Please try again.");
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    let shareNoteId = null;
    let selectedUserId = null;

    function openShareModal(noteId) {
        shareNoteId = noteId;
        selectedUserId = null;
        document.getElementById('recipientSearch').value = '';
        document.getElementById('userResults').innerHTML = '';
        document.getElementById('shareModal').style.display = 'block';
    }

    function closeShareModal() {
        document.getElementById('shareModal').style.display = 'none';
    }

    document.querySelectorAll('.share-button').forEach(button => {
        button.addEventListener('click', function() {
            const noteId = this.getAttribute('data-note-id');
            openShareModal(noteId);
        });
    });

    // Live search for users
    document.getElementById('recipientSearch').addEventListener('input', function() {
        const query = this.value.trim();
        const resultsDiv = document.getElementById('userResults');
        resultsDiv.innerHTML = '';
        selectedUserId = null;
        if (query.length === 0) return;
        fetch('/api/users?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                data.users.forEach(user => {
                    const item = document.createElement('button');
                    item.type = 'button';
                    item.className = 'list-group-item list-group-item-action';
                    item.textContent = user.username;
                    item.onclick = function() {
                        document.getElementById('recipientSearch').value = user.username;
                        selectedUserId = user.id;
                        resultsDiv.innerHTML = '';
                    };
                    resultsDiv.appendChild(item);
                });
            });
    });

    document.getElementById('confirmShareBtn').addEventListener('click', function() {
        if (!selectedUserId) {
            const alertDiv = document.getElementById('singleShareAlert');
            alertDiv.className = 'alert alert-danger';
            alertDiv.textContent = 'Please select a user to share with.';
            alertDiv.classList.remove('d-none');
            setTimeout(() => alertDiv.classList.add('d-none'), 4000);
            return;
        }
        fetch('/share_post', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({note_id: shareNoteId, recipient_id: selectedUserId})
        })
        .then(response => response.json())
        .then(data => {
            const alertDiv = document.getElementById('singleShareAlert');
            if (data.success) {
                alertDiv.className = 'alert alert-success';
                alertDiv.innerHTML = `<strong>Success!</strong> ${data.message || 'Post shared!'}`;
                alertDiv.classList.remove('d-none');
                closeShareModal();
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

    window.closeShareModal = closeShareModal;
});

document.addEventListener('DOMContentLoaded', function() {
    let selectedMultiUserId = null;

    // Show checkboxes and "Share Selected" button
    document.getElementById('shareMultipleBtn').addEventListener('click', function() {
        document.getElementById('Posts').classList.add('multi-share-mode');
        document.getElementById('shareSelectedBtn').classList.remove('d-none');
    });

    // Hide checkboxes and button when modal closes
    function closeMultiShareModal() {
        document.getElementById('multiShareModal').style.display = 'none';
        document.getElementById('Posts').classList.remove('multi-share-mode');
        document.getElementById('shareSelectedBtn').classList.add('d-none');
        document.querySelectorAll('.multi-share-checkbox').forEach(cb => cb.checked = false);
    }
    window.closeMultiShareModal = closeMultiShareModal;

    // When "Share Selected" is clicked, open modal if at least one post is checked
    document.getElementById('shareSelectedBtn').addEventListener('click', function() {
        const checked = document.querySelectorAll('.multi-share-checkbox:checked');
        if (checked.length === 0) {
            alert('Please select at least one post to share.');
            return;
        }
        selectedMultiUserId = null;
        document.getElementById('multiRecipientSearch').value = '';
        document.getElementById('multiUserResults').innerHTML = '';
        document.getElementById('multiShareModal').style.display = 'block';
    });

    // Live search for users for multi-share
    document.getElementById('multiRecipientSearch').addEventListener('input', function() {
        const query = this.value.trim();
        const resultsDiv = document.getElementById('multiUserResults');
        resultsDiv.innerHTML = '';
        selectedMultiUserId = null;
        if (query.length === 0) return;
        fetch('/api/users?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                data.users.forEach(user => {
                    const item = document.createElement('button');
                    item.type = 'button';
                    item.className = 'list-group-item list-group-item-action';
                    item.textContent = user.username;
                    item.onclick = function() {
                        document.getElementById('multiRecipientSearch').value = user.username;
                        selectedMultiUserId = user.id;
                        resultsDiv.innerHTML = '';
                    };
                    resultsDiv.appendChild(item);
                });
            });
    });

    document.getElementById('confirmMultiShareBtn').addEventListener('click', function() {
        if (!selectedMultiUserId) {
            alert('Please select a user to share with.');
            return;
        }
        const checked = Array.from(document.querySelectorAll('.multi-share-checkbox:checked')).map(cb => cb.value);
        if (checked.length === 0) {
            alert('Please select at least one post to share.');
            return;
        }
        fetch('/share_multiple_posts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({note_ids: checked, recipient_id: selectedMultiUserId})
        })
        .then(response => response.json())
        .then(data => {
            const alertDiv = document.getElementById('multiShareAlert');
            if (data.success) {
                alertDiv.className = 'alert alert-success';
                alertDiv.innerHTML = `
                    <strong>Success!</strong> ${data.shared} post(s) shared.<br>
                    ${data.ignored > 0 ? data.ignored + ' post(s) were already shared and ignored.' : ''}
                `;
                alertDiv.classList.remove('d-none');
                closeMultiShareModal();
                document.querySelectorAll('.multi-share-checkbox').forEach(cb => cb.checked = false);
            } else {
                alertDiv.className = 'alert alert-danger';
                alertDiv.textContent = data.error || 'Failed to share';
                alertDiv.classList.remove('d-none');
            }
            // Hide alert after 4 seconds
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

    window.closeMultiShareModal = closeMultiShareModal;
});
