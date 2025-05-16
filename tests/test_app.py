import sys
import os
from io import BytesIO
import unittest

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Note

class PrettyTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write("✔ PASS: %s\n" % self.getDescription(test))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write("✖ FAIL: %s\n" % self.getDescription(test))

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write("✖ ERROR: %s\n" % self.getDescription(test))

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_user(self, username, email, password='Testpass1!'):
        user = User(username=username, email=email)
        user.set_password(password)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        return user

    def login(self, email, password='Testpass1!'):
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def test_homepage_redirects_unauth(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_homepage_authenticated(self):
        self.create_user('hometester', 'hometester@example.com')
        self.login('hometester@example.com')
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"hometester" in response.data or b"Dashboard" in response.data or b"OZfoody" in response.data
        )

    def test_signup(self):
        signup_email = 'testsignup@example.com'
        signup_username = 'testsignupper'
        response = self.client.post('/sign_up', data={
            'username': signup_username,
            'email': signup_email,
            'password': 'Testpass1!',
            'confirm_password': 'Testpass1!',
            'profileImage': (BytesIO(b"dummy_profile_image_content"), 'test_profile.jpg')
        }, follow_redirects=True)
        with self.app.app_context():
            user = User.query.filter_by(email=signup_email).first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, signup_username)
        self.assertEqual(response.status_code, 200)
        found_expected_content = any(
            s in response.data for s in [
                b"Login", b"Account created successfully", b"Welcome",
                bytes(signup_username, 'utf-8'), b"Dashboard"
            ]
        )
        self.assertTrue(found_expected_content)

    def test_login_logout(self):
        self.create_user('testuser2', 'test2@example.com')
        response = self.login('test2@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"testuser2" in response.data or b"Dashboard" in response.data or b"Welcome" in response.data
        )
        logout_response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b"Login", logout_response.data)

    def test_duplicate_signup(self):
        self.create_user('dupuser', 'dup@example.com')
        response = self.client.post('/sign_up', data={
            'username': 'dupuser2',
            'email': 'dup@example.com',
            'password': 'Testpass1!',
            'confirm_password': 'Testpass1!',
            'profileImage': (BytesIO(b"dummy_profile_image_content"), 'dup_profile.jpg')
        }, follow_redirects=True)
        self.assertTrue(
            b'already registered' in response.data.lower() or
            b'already exists' in response.data.lower() or
            b'error' in response.data.lower()
        )

    def test_signup_password_mismatch(self):
        response = self.client.post('/sign_up', data={
            'username': 'mismatchuser',
            'email': 'mismatch@example.com',
            'password': 'Testpass1!',
            'confirm_password': 'Wrongpass!',
            'profileImage': (BytesIO(b"dummy_profile_image_content"), 'mismatch_profile.jpg')
        }, follow_redirects=True)
        self.assertTrue(
            b'passwords do not match' in response.data.lower() or
            b'error' in response.data.lower()
        )

    def test_create_and_view_post(self):
        user = self.create_user('poster', 'poster@example.com')
        self.login('poster@example.com')
        with self.app.app_context():
            initial_note_count = Note.query.count()
        post_data = {
            'Restaurant': 'Testaurant',
            'Review': 'Great food!',
            'Spiciness': 5,
            'Deliciousness': 5,
            'Value': 4,
            'Service': 5,
            'Stars': 5,
            'Cuisine': 'Test Cuisine',
            'location': 'Test Location',
            'image': (BytesIO(b"dummy_post_image_content"), 'test_post.jpg')
        }
        response = self.client.post('/new_post', data=post_data, follow_redirects=True, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertEqual(Note.query.count(), initial_note_count + 1)
            created_note = Note.query.filter_by(Restaurant='Testaurant', user_id=user.id).first()
            self.assertIsNotNone(created_note)
            self.assertEqual(created_note.Review, 'Great food!')
            self.assertEqual(created_note.location, 'Test Location')
            self.assertEqual(created_note.Cuisine, 'Test Cuisine')
            self.assertEqual(created_note.Stars, 5)
        self.assertIn(b"Testaurant", response.data)

    def test_edit_profile_invalid_email(self):
        user = self.create_user('edituser', 'edituser@example.com')
        self.login('edituser@example.com')
        response = self.client.post('/edit_profile', data={
            'username': 'editeduser',
            'email': 'not-an-email',
            'profileImage': (BytesIO(b"img"), 'profile.jpg')
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"invalid email" in response.data.lower() or
            b"error" in response.data.lower()
        )

    def test_edit_profile_duplicate_email(self):
        self.create_user('userA', 'userA@example.com')
        self.create_user('userB', 'userB@example.com')
        self.login('userA@example.com')
        response = self.client.post('/edit_profile', data={
            'username': 'userA',
            'email': 'userB@example.com',
            'profileImage': (BytesIO(b"img"), 'profile.jpg')
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"already registered" in response.data.lower() or
            b"already exists" in response.data.lower() or
            b"error" in response.data.lower()
        )

    def test_delete_nonexistent_post(self):
        self.create_user('deleter', 'deleter@example.com')
        self.login('deleter@example.com')
        response = self.client.post('/delete_post/9999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"not found" in response.data.lower() or
            b"error" in response.data.lower()
        )

    def test_view_profile_other_user(self):
        user1 = self.create_user('profile1', 'profile1@example.com')
        user2 = self.create_user('profile2', 'profile2@example.com')
        self.login('profile1@example.com')
        response = self.client.get(f'/user/{user2.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"profile2" in response.data or b"Profile" in response.data)

    def test_cannot_unfollow_not_following(self):
        user1 = self.create_user('alice2', 'alice2@example.com')
        user2 = self.create_user('bob2', 'bob2@example.com')
        self.login('alice2@example.com')
        response = self.client.post(f'/unfollow/{user2.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"not following" in response.data.lower() or
            b"follow" in response.data.lower() or
            b"error" in response.data.lower()
        )

    def test_post_invalid_data(self):
        user = self.create_user('invalidposter', 'invalidposter@example.com')
        self.login('invalidposter@example.com')
        post_data = {
            'Restaurant': '',
            'Review': '',
            'Spiciness': '',
            'Deliciousness': '',
            'Value': '',
            'Service': '',
            'Stars': '',
            'Cuisine': '',
            'location': '',
            'image': (BytesIO(b""), '')
        }
        response = self.client.post('/new_post', data=post_data, follow_redirects=True, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"required" in response.data.lower() or
            b"error" in response.data.lower() or
            b"invalid" in response.data.lower()
        )

    def test_access_nonexistent_user_profile(self):
        self.create_user('realuser', 'realuser@example.com')
        self.login('realuser@example.com')
        response = self.client.get('/user/9999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"not found" in response.data.lower() or
            b"error" in response.data.lower()
        )

    def test_follow_unfollow(self):
        user1 = self.create_user('alice', 'alice@example.com')
        user2 = self.create_user('bob', 'bob@example.com')
        self.login('alice@example.com')
        response = self.client.post(f'/follow/{user2.id}', follow_redirects=True)
        self.assertTrue(
            b"following" in response.data.lower() or
            response.status_code == 200
        )
        response = self.client.post(f'/unfollow/{user2.id}', follow_redirects=True)
        self.assertTrue(
            b"follow" in response.data.lower() or
            response.status_code == 200
        )

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2, resultclass=PrettyTestResult)
    unittest.main(testRunner=runner)
