# tests/base.py
import os
import unittest
from app import create_app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['ABLE'] = 'test_secret'
        self.app = create_app()
        self.app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

# tests/test_auth.py
import unittest
from app import db
from app.models import User


class AuthTestCase(BaseTestCase):
    def test_sign_up_password_mismatch(self):
        resp = self.client.post('/sign_up', data={
            'username': 'user1', 'email': 'u@example.com',
            'password': 'pass1', 'confirm_password': 'pass2'
        }, follow_redirects=True)
        self.assertIn(b'Passwords do not match', resp.data)

    def test_sign_up_duplicate_email(self):
        user = User(username='u1', email='u@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        resp = self.client.post('/sign_up', data={
            'username': 'u2', 'email': 'u@example.com',
            'password': 'pass', 'confirm_password': 'pass'
        }, follow_redirects=True)
        self.assertIn(b'already registered', resp.data)

# tests/test_models.py
import unittest
from app.models import User


class ModelTestCase(BaseTestCase):
    def test_password_hash_and_check(self):
        u = User(username='u', email='e@example.com')
        u.set_password('secret')
        self.assertNotEqual(u.password, 'secret')
        self.assertTrue(u.check_password('secret'))
        self.assertFalse(u.check_password('wrong'))

# tests/test_views.py
import unittest
import json

from app.models import User, Note

class ViewsTestCase(BaseTestCase):
    import io
    def create_user_and_login(self):
        self.client.post('/sign_up', data={
            'username': 'testu', 'email': 'test@x.com',
            'password': 'Test1234', 'confirm_password': 'Test1234'
        }, follow_redirects=True)

    def test_home_redirects(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/landing', resp.headers['Location'])
        self.create_user_and_login()
        resp2 = self.client.get('/', follow_redirects=False)
        self.assertEqual(resp2.status_code, 302)
        self.assertIn('/profile', resp2.headers['Location'])

    def test_landing_content(self):
        resp = self.client.get('/landing')
        self.assertEqual(resp.status_code, 200)
        # check for stats IDs rather than literal text
        self.assertIn(b'id="total-posts"', resp.data)
        self.assertIn(b'id="total-users"', resp.data)

    def test_profile_comment_and_view(self):
        resp = self.client.get('/profile')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login', resp.headers['Location'])
        self.create_user_and_login()
        # include dummy image upload to avoid UnboundLocalError
        image = (self.io.BytesIO(b"fake image"), 'test.jpg')
        resp_post = self.client.post('/new_post', data={
            'Restaurant':'R1','Cuisine':'C','Spiciness':'10',
            'Deliciousness':'20','Value':'30','Stars':'3','Service':'40','Review':'Nice',
            'image': image
        }, follow_redirects=True, content_type='multipart/form-data')
        user = User.query.filter_by(username='testu').first()
        note = Note.query.filter_by(user_id=user.id).first()
        resp2 = self.client.post('/profile', data={
            'Comment':'Great','user_id':user.id,'note_id':note.id,'parentID':0
        }, follow_redirects=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertIn(b'Great', resp2.data)

    def test_new_post_flow(self):
        resp = self.client.get('/new_post')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login', resp.headers['Location'])
        self.create_user_and_login()
        image = (self.io.BytesIO(b"fake image"), 'test2.jpg')
        resp2 = self.client.post('/new_post', data={
            'Restaurant':'R2','Cuisine':'C2','Spiciness':'50',
            'Deliciousness':'60','Value':'70','Stars':'4','Service':'80','Review':'Good',
            'image': image
        }, follow_redirects=True, content_type='multipart/form-data')
        self.assertEqual(resp2.status_code, 200)
        self.assertIn(b'R2', resp2.data)

    def test_api_reviews_pagination(self):
        self.create_user_and_login()
        for i in range(12):
            image = (self.io.BytesIO(b"fake"), f'{i}.jpg')
            self.client.post('/new_post', data={
                'Restaurant':f'R{i}','Cuisine':'X','Spiciness':'10',
                'Deliciousness':'10','Value':'10','Stars':'1','Service':'10','Review':'R',
                'image': image
            }, content_type='multipart/form-data')
        resp = self.client.get('/api/reviews')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 10)
        resp2 = self.client.get('/api/reviews?offset=10')
        data2 = json.loads(resp2.data)
        self.assertEqual(len(data2), 2)
