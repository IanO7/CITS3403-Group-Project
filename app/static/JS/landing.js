// Landing Page JavaScript
const progressBar = document.getElementById('progress-bar');
const unlockButton = document.getElementById('unlock-button');
const recommendationDiv = document.getElementById('recommendation');
const recommendationText = document.getElementById('recommendation-text');

if (unlockButton && progressBar) {
    unlockButton.addEventListener('click', () => {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = `${progress}%`;
            if (progress >= 100) {
                clearInterval(interval);
                fetch('/recommend_food')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const food = data.recommendations[0];
                            recommendationText.textContent = `${food.restaurant} - Spiciness: ${food.spiciness}, Deliciousness: ${food.deliciousness}`;
                            recommendationDiv.style.display = 'block';
                        }
                    });
            }
        }, 200);
    });
}

// Function to animate count up effect
function animateCountUp(element, target, duration = 1200) {
    if (!element || isNaN(target)) return; // Validate inputs
    let start = 0;
    const increment = target / (duration / 16);
    function update() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(update);
        } else {
            element.textContent = target;
        }
    }
    update();
}

// Intersection Observer to trigger animation when stats are visible
document.addEventListener('DOMContentLoaded', function () {
    const postsElem = document.getElementById('total-posts');
    const usersElem = document.getElementById('total-users');
    const statsElem = document.getElementById('stats');

    // Ensure elements exist
    if (!postsElem || !usersElem || !statsElem) {
        console.error('Required elements for stats animation are missing.');
        return;
    }

    // Replace template variables with actual values
    const postsTarget = parseInt(postsElem.dataset.target, 10) || 0; // Use data attributes for dynamic values
    const usersTarget = parseInt(usersElem.dataset.target, 10) || 0;

    let animated = false;

    function onEntry(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animateCountUp(postsElem, postsTarget);
                animateCountUp(usersElem, usersTarget);
                animated = true;
                observer.disconnect();
            }
        });
    }

    const observer = new IntersectionObserver(onEntry, { threshold: 0.5 });
    observer.observe(statsElem);
});


/*
To test this code, we need to:
    Simulate DOM elements (e.g., progress-bar, unlock-button, total-posts).
    Simulate user interactions (e.g., clicking the button).
    Mock API responses (e.g., /recommend_food).
    Verify the expected behavior (e.g., progress bar reaches 100%, recommendations are displayed, count-up animations work).
*/

/*
test('progress bar reaches 100% and displays recommendation', async () => {
    document.body.innerHTML = `
        <div id="progress-bar" style="width: 0;"></div>
        <button id="unlock-button"></button>
        <div id="recommendation" style="display: none;">
            <span id="recommendation-text"></span>
        </div>
    `;

    global.fetch = jest.fn(() =>
        Promise.resolve({
            json: () => Promise.resolve({ success: true, recommendations: [{ restaurant: 'Test Restaurant', spiciness: 5, deliciousness: 10 }] }),
        })
    );

    const unlockButton = document.getElementById('unlock-button');
    const progressBar = document.getElementById('progress-bar');
    const recommendationDiv = document.getElementById('recommendation');
    const recommendationText = document.getElementById('recommendation-text');

    unlockButton.click();

    // Wait for the progress bar to reach 100%
    await new Promise((resolve) => setTimeout(resolve, 2000));

    expect(progressBar.style.width).toBe('100%');
    expect(recommendationDiv.style.display).toBe('block');
    expect(recommendationText.textContent).toBe('Test Restaurant - Spiciness: 5, Deliciousness: 10');
});
*/