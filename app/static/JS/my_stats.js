document.addEventListener('DOMContentLoaded', () => {
    const foodChart = document.getElementById('foodChart');
    if (foodChart) {
        new Chart(foodChart.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Spicy', 'Delicious', 'Value', 'Service'],
                datasets: [{
                    data: [stats.spiciness, stats.deliciousness, stats.value, stats.service],
                    backgroundColor: ['#DF6F1B', '#5F8D3B', '#8E5F2B', '#6E3A14']
                }]
            }
        });
    }

    // Recommendation logic
    let recIndex = 0;
    let recs = [];
    const btn = document.getElementById('get-recommendation');
    const box = document.getElementById('recommended-food');

    function fetchRecs() {
        fetch('/recommend_food')
            .then(r => r.json())
            .then(data => {
                recs = data.recommendations;
                recIndex = 0;
                if (recs.length) {
                    box.innerHTML = renderPostCard(recs[recIndex++]);
                    btn.disabled = false;
                } else {
                    box.textContent = 'No recommendations found.';
                    btn.disabled = true;
                }
            });
    }

    btn?.addEventListener('click', () => {
        if (recIndex < recs.length) {
            box.innerHTML = renderPostCard(recs[recIndex++]);
            if (recIndex >= recs.length) {
                btn.disabled = true;
            }
        }
    });

    fetchRecs();

    // Search logic
    document.getElementById('search-button')?.addEventListener('click', () => {
        const query = document.getElementById('search-query').value.trim();
        fetch(`/api/search_reviews?q=${encodeURIComponent(query)}`)
            .then(r => r.json())
            .then(data => {
                const results = document.getElementById('search-results');
                results.innerHTML = '';
                if (data.results.length) {
                    data.results.forEach(post => {
                        results.innerHTML += renderPostCard(post);
                    });
                } else {
                    results.innerHTML = '<p class="text-muted">No results found.</p>';
                }
            });
    });
});

function renderPostCard(post) {
    return `
        <div class="recommendation-card">
            <h5>${post.restaurant}</h5>
            <p>${post.review}</p>
        </div>
    `;
}