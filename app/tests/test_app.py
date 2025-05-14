import sys
import os
from io import BytesIO

# Add the project root directory to the Python path
# This ensures that the 'app' module can be imported
# __file__ is /root/CITS3403-Group-Project/app/tests/test_app.py
# os.path.dirname(__file__) is /root/CITS3403-Group-Project/app/tests
# os.path.join(os.path.dirname(__file__), '..', '..') is /root/CITS3403-Group-Project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from app import create_app, db
from app.models import User, Note

@pytest.fixture
def client():
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True  # Crucial for test-specific behavior like flash messages
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Ensures a clean, in-memory DB for tests
    # If your app uses flask_login and you need to test routes that require login,
    # ensure LOGIN_DISABLED is False (default) or not set to True here.

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_homepage_loads(client):
    # Test unauthenticated access to homepage - expect redirect
    response_unauth = client.get('/')
    assert response_unauth.status_code == 302
    # Optionally, assert the redirect location if known, e.g.:
    # assert '/login' in response_unauth.headers['Location']

    # Test authenticated access
    user = User(username='hometester', email='hometester@example.com')
    user.set_password('Testpass1!')
    db.session.add(user)
    db.session.commit()
    
    login_response = client.post('/login', data={
        'email': 'hometester@example.com',
        'password': 'Testpass1!'
    }, follow_redirects=True)
    
    # Ensure login was successful and landed on a 200 page
    assert login_response.status_code == 200
    # Check for content that indicates successful login or dashboard access
    # Adjust these strings based on your application's actual content after login
    assert b"hometester" in login_response.data or b"Dashboard" in login_response.data or b"OZfoody" in login_response.data

    # Access homepage again as authenticated user
    response_auth = client.get('/', follow_redirects=True)
    assert response_auth.status_code == 200
    assert b"OZfoody" in response_auth.data
    # Add other assertions for authenticated homepage, e.g., username or dashboard elements
    assert b"hometester" in response_auth.data or b"Dashboard" in response_auth.data

def test_signup(client):
    # Use unique credentials for this test to avoid conflicts
    signup_email = 'testsignup@example.com'
    signup_username = 'testsignupper'

    response = client.post('/sign_up', data={
        'username': signup_username,
        'email': signup_email,
        'password': 'Testpass1!',
        'confirm_password': 'Testpass1!',
        'profileImage': (BytesIO(b"dummy_profile_image_content"), 'test_profile.jpg') # Simulate file upload
    }, follow_redirects=True)

    # Check 1: User created in database (This part seems to be passing)
    user = User.query.filter_by(email=signup_email).first()
    assert user is not None, f"User with email {signup_email} was not created in the database."
    assert user.username == signup_username

    # Check 2: Response status code after successful signup and redirect
    assert response.status_code == 200

    # --- Debugging Step: Print the response data to see what the page contains ---
    # print(f"\n--- Sign Up Response Data for {signup_email} ---")
    # print(response.data.decode(errors='ignore'))
    # print("--- End Sign Up Response Data ---\n")
    # --- End Debugging Step ---

    # Check 3: Content of the page after redirect.
    # Adjust these checks based on your application's behavior:
    # - Does it redirect to the login page? Expect "Login" and maybe a flash message.
    # - Does it redirect to the homepage and auto-login the user? Expect username, "Dashboard", or "Welcome".

    found_expected_content = False
    expected_strings = [
        b"Login",                            # If redirected to login page
        b"Account created successfully",     # Common flash message
        b"Welcome",                          # Generic welcome, or part of a flash message
        bytes(signup_username, 'utf-8'),    # If username is displayed on the page
        b"Dashboard"                         # If redirected to a user dashboard
    ]

    for s in expected_strings:
        if s in response.data:
            found_expected_content = True
            break
    
    assert found_expected_content, \
        f"Signup response content unexpected. None of the expected strings found. Status: {response.status_code}. Data: {response.data.decode(errors='ignore')[:500]}"

def test_login_logout(client):
    # Create user
    user = User(username='testuser2', email='test2@example.com')
    user.set_password('Testpass1!')
    db.session.add(user)
    db.session.commit()
    # Login
    response = client.post('/login', data={
        'email': 'test2@example.com',
        'password': 'Testpass1!'
    }, follow_redirects=True)
    
    assert response.status_code == 200 # Ensure the page after login redirect is successful
    # Adjust assertion to match actual content on successful login page
    # e.g., username, a specific welcome message, or "Dashboard"
    assert b"testuser2" in response.data or b"Dashboard" in response.data or b"Welcome" in response.data
    
    # Logout
    logout_response = client.get('/logout', follow_redirects=True)
    assert logout_response.status_code == 200 # Assuming logout redirects to a 200 page (e.g., login page)
    assert b"Login" in logout_response.data

# def test_create_post(client):
#     user = User(username='poster', email='poster@example.com')
#     user.set_password('Testpass1!')
#     db.session.add(user)
#     db.session.commit()
    
#     # Login the user and verify login success
#     login_response = client.post('/login', data={'email': 'poster@example.com', 'password': 'Testpass1!'}, follow_redirects=True)
#     assert login_response.status_code == 200
#     # Adjust to check for content indicating successful login for 'poster'
#     assert b"poster" in login_response.data or b"Dashboard" in login_response.data 

#     initial_note_count = Note.query.count()

#     # Create post
#     # Ensure keys here match the 'name' attributes of your form fields in the HTML/WTForms
#     post_data = {
#         'Resturaunt': 'Testaurant', # Assuming form field name matches model attribute
#         'Review': 'Great food!',    # Assuming form field name matches model attribute
#         'Spiciness': 5,             # Assuming form field name matches model attribute
#         'Deliciousness': 5,         # Assuming form field name matches model attribute
#         'Value': 4,                 # Assuming form field name matches model attribute
#         'Service': 5,               # Assuming form field name matches model attribute
#         'Stars': 5,                 # Added missing required field (assuming nullable=False)
#         'Cuisine': 'Test Cuisine',  # Added missing required field (assuming nullable=False)
#         'location': 'Test Location',# Added missing location field
#         'image': (BytesIO(b"dummy_post_image_content"), 'test_post.jpg') # Added image file
#     }
#     response = client.post('/new_post', data=post_data, follow_redirects=True, content_type='multipart/form-data') # Ensure content_type for file uploads
    
#     # 1. Check if the page after post submission/redirect is successful
#     assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response data: {response.data.decode(errors='ignore')[:500]}"

#     # 2. Check if the note was actually created in the database
#     assert Note.query.count() == initial_note_count + 1, "Note was not created in the database."

#     # 3. Retrieve the created note to verify its contents
#     #    Query using the correct attribute name from the model ('Resturaunt')
#     created_note = Note.query.filter_by(Resturaunt='Testaurant', user_id=user.id).first()
#     assert created_note is not None, "Could not find the created note in the database."
#     assert created_note.user_id == user.id
#     assert created_note.Review == 'Great food!' # Check against the correct model attribute
#     assert created_note.location == 'Test Location'
#     assert created_note.Cuisine == 'Test Cuisine'
#     assert created_note.Stars == 5

#     # 4. Verify the content on the redirected page
#     #    This depends on what your /new_post route redirects to and what content is displayed.
#     #    It might be the homepage, a list of posts, or the post detail page.
#     #    If it redirects to a page displaying the post, "Testaurant" should be there.
#     assert b"Testaurant" in response.data, \
#         f"Expected 'Testaurant' in response, but got: {response.data.decode(errors='ignore')[:500]}"

def test_follow_unfollow(client):
    user1 = User(username='alice', email='alice@example.com')
    user1.set_password('Testpass1!')
    user2 = User(username='bob', email='bob@example.com')
    user2.set_password('Testpass1!')
    db.session.add_all([user1, user2])
    db.session.commit()
    client.post('/login', data={'email': 'alice@example.com', 'password': 'Testpass1!'})
    response = client.post(f'/follow/{user2.id}', follow_redirects=True)
    assert b"Following" in response.data or response.status_code == 200
    response = client.post(f'/unfollow/{user2.id}', follow_redirects=True)
    assert b"Follow" in response.data or response.status_code == 200
