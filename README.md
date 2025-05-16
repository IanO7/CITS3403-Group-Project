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

> **Note for Windows users:**  
> Make sure to open your Ubuntu (WSL) terminal before running the following commands.  
> All setup and `flask run` commands should be executed inside your Ubuntu (WSL) environment, not in Windows CMD or PowerShell.

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

---

> **🔥 Hot Tip:**  
> For best results and to avoid Python system errors, always use a virtual environment for your project dependencies.  
> This is now required on modern Ubuntu/WSL.
>
> **First time only (if not already installed):**
> ```sh
> sudo apt update
> sudo apt install python3-venv
> ```
> **Then, for every new project or fresh clone:**
> ```sh
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> ```
> Your `venv/` folder is local!
> After cloning a new repo, always create and activate a new virtual environment, then install dependencies.

---

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/OZfoody.git
    cd OZfoody
    ```

2. **(Recommended) Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    ```sh
    flask db upgrade
    ```

5. **(Optional) Load demo users and posts:**
    ```sh
    python demo/seed_demo_data.py
    ```
    This will create several demo users and posts. You can log in as any demo user, view their posts, share posts, and make friends with other demo accounts.

6. **(Optional) Clean demo data before closing or for a fresh start:**
    ```sh
    python demo/clean_demo_data.py
    ```
    This will remove all demo users and their posts.

7. **Run the app:**
    ```sh
    flask run
    ```

*Made for CITS3403 at UWA.*