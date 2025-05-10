// Follow/Unfollow a user and toggle posts visibility
document.querySelectorAll('.follow-button').forEach(button => {
    button.addEventListener('click', () => {
        const userId = button.getAttribute('data-user-id');
        const isFollowing = button.classList.contains('btn-danger');
        const url = isFollowing ? `/unfollow/${userId}` : `/follow/${userId}`;
        const method = 'POST';

        fetch(url, { method })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle button appearance and text
                    button.classList.toggle('btn-success');
                    button.classList.toggle('btn-danger');
                    button.textContent = isFollowing ? 'Follow' : 'Unfollow';

                    // Show or hide posts for the user
                    document.querySelectorAll(`.user-post[data-user-id="${userId}"]`).forEach(post => {
                        post.style.display = isFollowing ? 'none' : 'block';
                    });
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    });
});

// Like/Unlike a post and update the likes count dynamically
document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
        const noteId = button.getAttribute('data-note-id');
        fetch(`/like/${noteId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const likeCount = button.querySelector('.action-count');
                    likeCount.textContent = data.likes; // Update the likes count dynamically
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    });
});

// Search suggestions
const searchInput = document.getElementById('search-input');
const suggestionsBox = document.getElementById('suggestions');

searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim();
    if (query.length === 0) {
        suggestionsBox.innerHTML = '';
        return;
    }

    // Fetch suggestions from the backend

    /**
     * Problem: Some fetch requests lack proper error handling 
     * for failed network requests or invalid responses.
     * Fix: Add .catch blocks to all fetch requests to log errors 
     * and handle them gracefully.
     */
    fetch(`/api/search_suggestions?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                suggestionsBox.innerHTML = data.suggestions.map(username => `
                    <a href="/search_users?q=${encodeURIComponent(username)}" class="list-group-item list-group-item-action">
                        ${username}
                    </a>
                `).join('');
            }
        })
        .catch(error => console.error('Error fetching search suggestions:', error));
});

// Hide suggestions when clicking outside
/** 
    * Problem: The click event listener for hiding suggestions 
    * may throw an error if searchInput or suggestionsBox is null.
    * Fix: Add null checks for searchInput and suggestionsBox 
    * before adding event listeners.
*/
if (searchInput && suggestionsBox) {
    document.addEventListener('click', (event) => {
        if (!searchInput.contains(event.target) && !suggestionsBox.contains(event.target)) {
            suggestionsBox.innerHTML = '';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const trendingContainer = document.getElementById('trending-dishes-container');

    // Fetch trending dishes from the backend
    fetch('/trending_dishes')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const dishes = data.dishes;

                // Highlight the most liked dish
                dishes.forEach((dish, index) => {
                    const dishCard = `
                        <div class="dish-card ${index === 0 ? 'trending' : ''}">
                            <img src="${dish.image || 'https://via.placeholder.com/300'}" alt="${dish.restaurant}">
                            <h5>${dish.restaurant}</h5>
                            <p>${dish.review}</p>
                            <p class="likes">❤️ ${dish.likes} Likes</p>
                            <p>Spiciness: ${dish.spiciness}, Deliciousness: ${dish.deliciousness}, Value: ${dish.value}, Plating: ${dish.plating}</p>
                        </div>
                    `;
                    trendingContainer.innerHTML += dishCard;
                });
            } else {
                trendingContainer.innerHTML = '<p class="text-muted text-center">No trending dishes found.</p>';
            }
        })
        .catch(error => console.error('Error fetching trending dishes:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    const postsContainer = document.getElementById('merged-posts-container');
    const recommendationsContainer = document.getElementById('recommendations-container');

    // Fetch merged posts
    fetch('/merged_posts')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const posts = data.posts;

                // Display merged posts
                posts.forEach(post => {
                    const postCard = `
                        <div class="post-card ${post.is_special ? 'special' : ''}">
                            <img src="${post.image || 'https://via.placeholder.com/300'}" alt="${post.restaurant}">
                            <h5>${post.restaurant}</h5>
                            <p>${post.review}</p>
                            <p class="likes">❤️ ${post.likes} Likes</p>
                            <p>Spiciness: ${post.spiciness}, Deliciousness: ${post.deliciousness}, Value: ${post.value}, Plating: ${post.plating}</p>
                            <p><strong>Location:</strong> ${post.location || "Not specified"}</p>
                        </div>
                    `;
                    postsContainer.innerHTML += postCard;
                });

                // Display swipeable recommendations (same as posts but in a swipeable format)
                posts.forEach(post => {
                    const recommendationCard = `
                        <div class="recommendation-card ${post.is_special ? 'special' : ''}">
                            <img src="${post.image || 'https://via.placeholder.com/300'}" alt="${post.restaurant}">
                            <h5>${post.restaurant}</h5>
                            <p>${post.review}</p>
                            <p class="likes">❤️ ${post.likes} Likes</p>
                            <p>Spiciness: ${post.spiciness}, Deliciousness: ${post.deliciousness}, Value: ${post.value}, Plating: ${post.plating}</p>
                            <p><strong>Location:</strong> ${post.location || "Not specified"}</p>
                        </div>
                    `;
                    recommendationsContainer.innerHTML += recommendationCard;
                });
            } else {
                postsContainer.innerHTML = '<p class="text-muted text-center">No posts found.</p>';
                recommendationsContainer.innerHTML = '<p class="text-muted text-center">No recommendations found.</p>';
            }
        })
        .catch(error => console.error('Error fetching posts:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.getElementById('recommendations-carousel');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    let currentIndex = 0;

    // Fetch posts
    fetch('/merged_posts')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const posts = data.posts;

                // Populate the carousel
                posts.forEach(post => {
                    const recommendationCard = `
                        <div class="recommendation-card ${post.is_special ? 'special' : ''}">
                            <img src="${post.image || 'https://via.placeholder.com/300'}" alt="${post.restaurant}">
                            <h5>${post.restaurant}</h5>
                            <p>${post.review}</p>
                            <p class="likes">❤️ ${post.likes} Likes</p>
                            <p>Spiciness: ${post.spiciness}, Deliciousness: ${post.deliciousness}, Value: ${post.value}, Plating: ${post.plating}</p>
                            <p><strong>Location:</strong> ${post.location || "Not specified"}</p>
                        </div>
                    `;
                    carousel.innerHTML += recommendationCard;
                });

                // Set initial position
                updateCarousel();
            } else {
                carousel.innerHTML = '<p class="text-muted text-center">No posts found.</p>';
            }
        })
        .catch(error => console.error('Error fetching posts:', error));

    // Update carousel position
    function updateCarousel() {
        const cards = document.querySelectorAll('.recommendation-card');
        cards.forEach((card, index) => {
            card.style.transform = `translateX(${(index - currentIndex) * 100}%)`;
        });
    }

    // Previous button
    prevBtn.addEventListener('click', () => {
        const cards = document.querySelectorAll('.recommendation-card');
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    });

    // Next button
    nextBtn.addEventListener('click', () => {
        const cards = document.querySelectorAll('.recommendation-card');
        if (currentIndex < cards.length - 1) {
            currentIndex++;
            updateCarousel();
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.getElementById('friend-posts-carousel');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    let currentIndex = 0;

    // Fetch posts from followed friends
    fetch('/friend_posts')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const posts = data.posts;

                // Populate the carousel
                posts.forEach(post => {
                    const recommendationCard = `
                        <div class="recommendation-card">
                            <img src="${post.image || 'https://via.placeholder.com/300'}" alt="${post.restaurant}">
                            <h5>${post.restaurant}</h5>
                            <p>${post.review}</p>
                            <p class="likes">❤️ ${post.likes} Likes</p>
                            <p>Spiciness: ${post.spiciness}, Deliciousness: ${post.deliciousness}, Value: ${post.value}, Plating: ${post.plating}</p>
                            <p><strong>Location:</strong> ${post.location || "Not specified"}</p>
                        </div>
                    `;
                    carousel.innerHTML += recommendationCard;
                });

                // Set initial position
                updateCarousel();
            } else {
                carousel.innerHTML = '<p class="text-muted text-center">No posts found.</p>';
            }
        })
        .catch(error => console.error('Error fetching posts:', error));

    // Update carousel position
    function updateCarousel() {
        const cards = document.querySelectorAll('.recommendation-card');
        cards.forEach((card, index) => {
            card.style.transform = `translateX(${(index - currentIndex) * 100}%)`;
        });
    }

    // Previous button
    prevBtn.addEventListener('click', () => {
        const cards = document.querySelectorAll('.recommendation-card');
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    });

    // Next button
    nextBtn.addEventListener('click', () => {
        const cards = document.querySelectorAll('.recommendation-card');
        if (currentIndex < cards.length - 1) {
            currentIndex++;
            updateCarousel();
        }
    });
});

// Ensure the server injects a JSON object into a script tag
const myStats = JSON.parse('{{ user_stats | tojson | safe }}');

// Fallback values in case the server does not provide data
const stats = {
    spiciness: myStats.spiciness || 0,
    deliciousness: myStats.deliciousness || 0,
    value: myStats.value || 0,
    plating: myStats.plating || 0,
    post: typeof userNotesLength !== 'undefined' ? userNotesLength : 0
};

document.addEventListener('DOMContentLoaded', function() {
    // Fill in your stats
    document.getElementById('my-spiciness').textContent = Math.round(stats.spiciness);
    document.getElementById('my-deliciousness').textContent = Math.round(stats.deliciousness);
    document.getElementById('my-value').textContent = Math.round(stats.value);
    document.getElementById('my-plating').textContent = Math.round(stats.plating);
    document.getElementById('my-posts').textContent = stats.posts;

    // Friend search logic
    const searchInput = document.getElementById('friend-compare-search');
    const suggestionsBox = document.getElementById('friend-compare-suggestions');
    const compareTable = document.getElementById('compare-stats-table');
    const friendNameHeader = document.getElementById('friend-name-header');

    let lastQuery = '';
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        if (query.length === 0) {
            suggestionsBox.innerHTML = '';
            compareTable.style.display = 'none';
            return;
        }
        lastQuery = query;
        fetch(`/api/users?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                if (data.users && data.users.length > 0) {
                    suggestionsBox.innerHTML = data.users.map(u =>
                        `<div class="list-group-item" data-id="${u.id}" data-username="${u.username}">${u.username}</div>`
                    ).join('');
                } else {
                    suggestionsBox.innerHTML = '<div class="list-group-item text-muted">No users found</div>';
                }
            });
    });

    // Handle suggestion click
    suggestionsBox.addEventListener('click', function(e) {
        const item = e.target.closest('.list-group-item[data-id]');
        if (item) {
            const friendId = item.getAttribute('data-id');
            const friendName = item.getAttribute('data-username');
            searchInput.value = friendName;
            suggestionsBox.innerHTML = '';
            fetch(`/api/user_stats/${friendId}`)
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        compareTable.style.display = '';
                        friendNameHeader.textContent = data.username;
                        document.getElementById('friend-spiciness').textContent = Math.round(data.stats.spiciness);
                        document.getElementById('friend-deliciousness').textContent = Math.round(data.stats.deliciousness);
                        document.getElementById('friend-value').textContent = Math.round(data.stats.value);
                        document.getElementById('friend-plating').textContent = Math.round(data.stats.plating);
                        document.getElementById('friend-posts').textContent = data.posts;
                    }
                });
        }
    });

    // Hide suggestions when clicking outside
    if (searchInput && suggestionsBox) {
        document.addEventListener('click', (event) => {
            if (!searchInput.contains(event.target) && !suggestionsBox.contains(event.target)) {
                suggestionsBox.innerHTML = '';
            }
        });
    }
});