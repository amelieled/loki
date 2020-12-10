import unittest

from flask_testing import TestCase
from flask_login import current_user

from loki import app, db
from loki.models import User


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config['DEBUG '] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "ad@min.com", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """A test case for all actions made by a non-authenticated client"""

    def test_home(self):
        response = self.client.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home.html')
        self.assert_context("title", "Home")

    def test_about(self):
        response = self.client.get('/about', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('about.html')
        self.assert_context("title", "About")

    def test_login(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')
        self.assert_context("title", "Log in")

    def test_register(self):
        response = self.client.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('register.html')
        self.assert_context("title", "Register")

    def test_account(self):
        response = self.client.get('/account', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')
        self.assert_context("title", "Log in")
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_logout(self):
        response = self.client.get('/logout', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')
        self.assert_context("title", "Log in")
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_model_upload(self):
        response = self.client.get('/models/upload', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')
        self.assert_context("title", "Log in")
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_model_predict(self):
        response = self.client.get('/models/predict', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')
        self.assert_context("title", "Log in")
        self.assertIn(b'Please log in to access this page.', response.data)
    
    def test_attacks_visualize(self):
        response = self.client.get('/attacks/visualize', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')
        self.assert_context("title", "Log in")
        self.assertIn(b'Please log in to access this page.', response.data)


class LoginAndOutTests(BaseTestCase):
    """A test case for actions on the login and logout route"""

    # Ensure login behaves correctly with empty email
    def test_incorrect_login_email_empty(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="", password="admin"),
                follow_redirects=True
            )
            self.assertIn(b'This field is required.', response.data)
            self.assertFalse(current_user.is_active)
            self.assertFalse(current_user.is_authenticated)

    # Ensure login behaves correctly with invalid email
    def test_incorrect_login_email_invalid(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="invalidemail", password="admin"),
                follow_redirects=True
            )
            self.assertIn(b'Invalid email address.', response.data)
            self.assertFalse(current_user.is_active)
            self.assertFalse(current_user.is_authenticated)
    
    # Ensure login behaves correctly with empty password
    def test_incorrect_login_password_empty(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="valid@email.com", password=""),
                follow_redirects=True
            )
            self.assertIn(b'This field is required.', response.data)
            self.assertFalse(current_user.is_active)
            self.assertFalse(current_user.is_authenticated)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You are logged in!' , response.data)
            self.assertTrue(current_user.is_active)
            self.assertTrue(current_user.is_authenticated)

    # Ensure login behaves correctly with invalid credentials
    def test_incorrect_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="wrong@gmail.com", password="wrong"),
                follow_redirects=True
            )
            self.assertIn(b'Login unsuccessful!', response.data)
            self.assertFalse(current_user.is_active)
            self.assertFalse(current_user.is_authenticated)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You are logged out!', response.data)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_active)
            self.assertFalse(current_user.is_authenticated)


if __name__ == '__main__':
    unittest.main()