# OZfoody

OZfoody is a social restaurant review platform for discovering, sharing, and discussing food experiences with friends. Share your reviews, earn badges, follow friends, and get personalized food recommendations!

## Features

- **User Authentication:** Sign up, log in, and manage your profile.
- **Restaurant Reviews:** Post reviews with ratings for spiciness, deliciousness, value, service, and more.
- **Photo Uploads:** Add images to your reviews.
- **Friend System:** Follow/unfollow users, approve follow requests, and see friends' posts.
- **Personalized Dashboard:** View your food stats, achievements, and get food recommendations.
- **Badges & Levels:** Earn badges and level up as you contribute.
- **Trending Dishes:** See what's popular in the community.
- **Search:** Find users and search reviews by keywords.
- **Post Sharing:** Share your posts with friends directly.
- **Responsive UI:** Modern, mobile-friendly design using Bootstrap.

## Project Structure

```
app/
    __init__.py
    auth.py
    config.py
    models.py
    views.py
    routes/
        auth.py
    static/
        css/
        image/
        JS/
    templates/
        base.html
        landing.html
        my_stats.html
        my_friends.html
        profile.html
        ...
    uploads/
migrations/
main.py
requirements.txt
README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/OZfoody.git
    cd OZfoody
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up the database:**
    ```sh
    flask db upgrade
    ```

4. **Run the app:**
    ```sh
    flask run
    ```
    Or, if using `main.py`:
    ```sh
    python main.py
    ```

5. **Visit:**  
    Open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

- **Sign up** for a new account.
- **Create reviews** for restaurants you visit.
- **Follow friends** to see their food adventures.
- **Earn badges** and show it off.
- **Search** for users or reviews.
- **Share posts** with your friends.

## License

[MIT](LICENSE)

---

*Made for CITS3403 at UWA.*