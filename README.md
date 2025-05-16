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

Name            Student number  Github Username
Divyank Sharma  23810783        divxsharma
Ian Oon         23722317        IanO7
Vanilla Tran    24060828        cipherbunnie
Isabel Newlands 23803298        eye4c

```
app/
    __init__.py
    auth.py
    models.py
    views.py
    
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
        editpost.html
        login.html
        signup.html
        my_friends.html
        my_stats.html
        settings.html
        user_profile.html
        inbox.html
        newpost.html
        others_stats.html
        post.html
        search_results.html
        ...
    uploads/
instance/
    database.db
migrations/
tests/
    selenium/
       ... 
    __init__.py
    test_app.py
    unitTests.py
.gitignore
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
> 
> **IDE Tip:**  
> After creating and activating your virtual environment, make sure your code editor (e.g., VS Code, PyCharm) is using the Python interpreter from your `venv` folder.  
> In VS Code, open the Command Palette (`Ctrl+Shift+P`), search for `Python: Select Interpreter`, and choose the one from your project's `venv` directory.  
> This ensures all installed packages are recognized and avoids import errors.

---

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/IanO7/CITS3403-Group-Project.git
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

---

## Selenium Testing

Automated UI tests are provided using Selenium IDE and Python scripts.

**To run Selenium tests:**

1. **Always clean and reseed demo data before running Selenium tests:**
    ```sh
    python demo/clean_demo_data.py
    python demo/seed_demo_data.py
    ```

2. **Start the Flask app:**
    ```sh
    flask run
    ```

3. **Open Selenium IDE** (install from [selenium.dev](https://www.selenium.dev/selenium-ide/)).

4. **Open the `CITS3403 Group Project.side` test file** provided in the repo.

5. **Run all tests** in Selenium IDE.

- If you want to repeat the tests, always clean and reseed demo data first, as some tests (like password change) will permanently alter the database.

- Python-based Selenium test scripts and reports are also included in the repo for reference.

---

*Made for CITS3403 at UWA.*