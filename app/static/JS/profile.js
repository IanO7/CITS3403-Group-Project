document.addEventListener('DOMContentLoaded', function() {
    const shareMultipleBtn = document.getElementById('shareMultipleBtn');
    if (shareMultipleBtn) {
        shareMultipleBtn.addEventListener('click', function () {
            const checkboxes = document.querySelectorAll('.multi-share-checkbox');
            checkboxes.forEach(container => {
                container.style.display = container.style.display === 'none' ? 'block' : 'none';
            });
        });
    }

    const shareSelectedBtn = document.getElementById('shareSelectedBtn');
    if (shareSelectedBtn) {
        shareSelectedBtn.addEventListener('click', function () {
            const checkboxes = document.querySelectorAll('.multi-share-checkbox');
            checkboxes.forEach(container => {
                container.style.display = container.style.display === 'none' ? 'block' : 'none';
            });
        });
    }

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
                            // Assuming showOzfoodyNotification is globally available
                            if (typeof showOzfoodyNotification === 'function') {
                                showOzfoodyNotification("Post deleted successfully!", "success");
                            } else {
                                alert("Post deleted successfully!");
                            }
                            setTimeout(() => location.reload(), 1500); // Reload after a short delay
                        } else {
                             if (typeof showOzfoodyNotification === 'function') {
                                showOzfoodyNotification("Failed to delete the post. Please try again.", "error");
                            } else {
                                alert("Failed to delete the post. Please try again.");
                            }
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    });

    // Single post share functionality
    let shareNoteId = null;
    let selectedUserId = null;

    function openShareModal(noteId) {
        shareNoteId = noteId;
        selectedUserId = null;
        const recipientSearch = document.getElementById('recipientSearch');
        if (recipientSearch) recipientSearch.value = '';
        const userResults = document.getElementById('userResults');
        if (userResults) userResults.innerHTML = '';
        const shareModal = document.getElementById('shareModal');
        if (shareModal) shareModal.style.display = 'block';
    }

    function closeShareModal() {
        const shareModal = document.getElementById('shareModal');
        if (shareModal) shareModal.style.display = 'none';
    }
    window.closeShareModal = closeShareModal; // Make it globally accessible for inline onclick

    document.querySelectorAll('.share-button').forEach(button => {
        button.addEventListener('click', function() {
            const noteId = this.getAttribute('data-note-id');
            openShareModal(noteId);
        });
    });

    const recipientSearchInput = document.getElementById('recipientSearch');
    if (recipientSearchInput) {
        recipientSearchInput.addEventListener('input', function() {
            const query = this.value.trim();
            const resultsDiv = document.getElementById('userResults');
            if (!resultsDiv) return;
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
                            if (recipientSearchInput) recipientSearchInput.value = user.username;
                            selectedUserId = user.id;
                            resultsDiv.innerHTML = '';
                        };
                        resultsDiv.appendChild(item);
                    });
                });
        });
    }

    const confirmShareBtn = document.getElementById('confirmShareBtn');
    if (confirmShareBtn) {
        confirmShareBtn.addEventListener('click', function() {
            if (!selectedUserId) {
                // Assuming showOzfoodyNotification is globally available
                if (typeof showOzfoodyNotification === 'function') {
                    showOzfoodyNotification('Please select a user to share with.', 'error');
                } else {
                    alert('Please select a user to share with.');
                }
                return;
            }
            fetch('/share_post', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({note_id: shareNoteId, recipient_id: selectedUserId})
            })
            .then(response => response.json())
            .then(data => {
                const alertDiv = document.getElementById('singleShareAlert'); // Or use showOzfoodyNotification
                if (data.success) {
                    if (alertDiv) {
                        alertDiv.className = 'alert alert-success';
                        alertDiv.innerHTML = `<strong>Success!</strong> ${data.message || 'Post shared!'}`;
                        alertDiv.classList.remove('d-none');
                        setTimeout(() => alertDiv.classList.add('d-none'), 4000);
                    } else if (typeof showOzfoodyNotification === 'function') {
                        showOzfoodyNotification(data.message || 'Post shared!', 'success');
                    }
                    closeShareModal();
                } else {
                    if (alertDiv) {
                        alertDiv.className = 'alert alert-danger';
                        alertDiv.textContent = data.error || 'Failed to share';
                        alertDiv.classList.remove('d-none');
                        setTimeout(() => alertDiv.classList.add('d-none'), 4000);
                    } else if (typeof showOzfoodyNotification === 'function') {
                        showOzfoodyNotification(data.error || 'Failed to share', 'error');
                    }
                }
            })
            .catch(() => {
                const alertDiv = document.getElementById('singleShareAlert');
                 if (alertDiv) {
                    alertDiv.className = 'alert alert-danger';
                    alertDiv.textContent = 'Failed to share due to a network error.';
                    alertDiv.classList.remove('d-none');
                    setTimeout(() => alertDiv.classList.add('d-none'), 4000);
                } else if (typeof showOzfoodyNotification === 'function') {
                    showOzfoodyNotification('Failed to share due to a network error.', 'error');
                }
            });
        });
    }

    // Multi-post share functionality
    let selectedMultiUserId = null;
    const multiShareMultipleBtn = document.getElementById('shareMultipleBtn'); // Renamed to avoid conflict
    const multiShareSelectedBtn = document.getElementById('shareSelectedBtn'); // Renamed to avoid conflict
    const postsContainer = document.getElementById('Posts');

    if (multiShareMultipleBtn && multiShareSelectedBtn && postsContainer) {
        multiShareMultipleBtn.addEventListener('click', function(event) {
            event.stopPropagation();
            postsContainer.classList.add('multi-share-mode');
            multiShareSelectedBtn.classList.remove('d-none');
        });

        function closeMultiShareModal() {
            const multiShareModal = document.getElementById('multiShareModal');
            if (multiShareModal) multiShareModal.style.display = 'none';
            postsContainer.classList.remove('multi-share-mode');
            multiShareSelectedBtn.classList.add('d-none');
            document.querySelectorAll('.multi-share-checkbox').forEach(cb => cb.checked = false);
        }
        window.closeMultiShareModal = closeMultiShareModal; // Make it globally accessible

        multiShareSelectedBtn.addEventListener('click', function(event) {
            event.stopPropagation();
            const checked = document.querySelectorAll('.multi-share-checkbox:checked');
            if (checked.length === 0) {
                if (typeof showOzfoodyNotification === 'function') {
                    showOzfoodyNotification('Please select at least one post to share.', 'error');
                } else {
                    alert('Please select at least one post to share.');
                }
                return;
            }
            selectedMultiUserId = null;
            const multiRecipientSearch = document.getElementById('multiRecipientSearch');
            if (multiRecipientSearch) multiRecipientSearch.value = '';
            const multiUserResults = document.getElementById('multiUserResults');
            if (multiUserResults) multiUserResults.innerHTML = '';
            const multiShareModal = document.getElementById('multiShareModal');
            if (multiShareModal) multiShareModal.style.display = 'block';
        });

        const multiRecipientSearchInput = document.getElementById('multiRecipientSearch');
        if (multiRecipientSearchInput) {
            multiRecipientSearchInput.addEventListener('input', function() {
                const query = this.value.trim();
                const resultsDiv = document.getElementById('multiUserResults');
                if (!resultsDiv) return;
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
                                if (multiRecipientSearchInput) multiRecipientSearchInput.value = user.username;
                                selectedMultiUserId = user.id;
                                resultsDiv.innerHTML = '';
                            };
                            resultsDiv.appendChild(item);
                        });
                    });
            });
        }

        const confirmMultiShareBtn = document.getElementById('confirmMultiShareBtn');
        if (confirmMultiShareBtn) {
            confirmMultiShareBtn.addEventListener('click', function() {
                if (!selectedMultiUserId) {
                    if (typeof showOzfoodyNotification === 'function') {
                        showOzfoodyNotification('Please select a user to share with.', 'error');
                    } else {
                        alert('Please select a user to share with.');
                    }
                    return;
                }
                const checked = Array.from(document.querySelectorAll('.multi-share-checkbox:checked')).map(cb => cb.value);
                if (checked.length === 0) {
                     if (typeof showOzfoodyNotification === 'function') {
                        showOzfoodyNotification('Please select at least one post to share.', 'error');
                    } else {
                        alert('Please select at least one post to share.');
                    }
                    return;
                }
                fetch('/share_multiple_posts', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({note_ids: checked, recipient_id: selectedMultiUserId})
                })
                .then(response => response.json())
                .then(data => {
                    const alertDiv = document.getElementById('multiShareAlert'); // Or use showOzfoodyNotification
                    if (data.success) {
                        if (alertDiv) {
                            alertDiv.className = 'alert alert-success';
                            alertDiv.innerHTML = `
                                <strong>Success!</strong> ${data.shared} post(s) shared.<br>
                                ${data.ignored > 0 ? data.ignored + ' post(s) were already shared and ignored.' : ''}
                            `;
                            alertDiv.classList.remove('d-none');
                            setTimeout(() => alertDiv.classList.add('d-none'), 4000);
                        } else if (typeof showOzfoodyNotification === 'function') {
                             let message = `${data.shared} post(s) shared.`;
                             if (data.ignored > 0) {
                                 message += ` ${data.ignored} post(s) were already shared and ignored.`;
                             }
                            showOzfoodyNotification(message, 'success');
                        }
                        closeMultiShareModal();
                        document.querySelectorAll('.multi-share-checkbox').forEach(cb => cb.checked = false);
                    } else {
                        if (alertDiv) {
                            alertDiv.className = 'alert alert-danger';
                            alertDiv.textContent = data.error || 'Failed to share';
                            alertDiv.classList.remove('d-none');
                            setTimeout(() => alertDiv.classList.add('d-none'), 4000);
                        } else if (typeof showOzfoodyNotification === 'function') {
                            showOzfoodyNotification(data.error || 'Failed to share', 'error');
                        }
                    }
                })
                .catch(() => {
                    const alertDiv = document.getElementById('multiShareAlert');
                    if (alertDiv) {
                        alertDiv.className = 'alert alert-danger';
                        alertDiv.textContent = 'Failed to share due to a network error.';
                        alertDiv.classList.remove('d-none');
                        setTimeout(() => alertDiv.classList.add('d-none'), 4000);
                    } else if (typeof showOzfoodyNotification === 'function') {
                        showOzfoodyNotification('Failed to share due to a network error.', 'error');
                    }
                });
            });
        }

        document.addEventListener('click', function(event) {
            if (!multiShareSelectedBtn.classList.contains('d-none')) { // Only act if multi-share is active
                const isClickInsideShareMultipleBtn = multiShareMultipleBtn.contains(event.target);
                const isClickInsideShareSelectedBtn = multiShareSelectedBtn.contains(event.target);
                // Check if the click is inside any element that should keep multi-share active
                // This includes the posts container (for clicking checkboxes) and the multi-share modal itself
                const isClickInsideMultiShareArea = postsContainer.contains(event.target) || 
                                                    (document.getElementById('multiShareModal') && document.getElementById('multiShareModal').contains(event.target));

                if (!isClickInsideShareMultipleBtn && !isClickInsideShareSelectedBtn && !isClickInsideMultiShareArea) {
                    postsContainer.classList.remove('multi-share-mode');
                    multiShareSelectedBtn.classList.add('d-none');
                    // Uncheck all multi-share checkboxes
                    document.querySelectorAll('.multi-share-checkbox').forEach(cb => cb.checked = false);
                }
            }
        });
    }
});