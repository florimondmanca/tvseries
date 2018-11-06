"""Test signing up as a new user."""
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import TestCase

User = get_user_model()


class BaseSignupTest:
    """Base signup test case.

    The actual test case is defined as a static nested class to avoid
    unittest picking it up as an actual test.
    """

    class TestCase(TestCase):
        __SIGNUP_PAGE_URL = '/accounts/signup/'

        def _visit_signup(self):
            return self.client.get(self.__SIGNUP_PAGE_URL)

        def _signup(self, **kwargs):
            data = {
                'username': 'johndoe',
                'password1': 'onions88',
                'password2': 'onions88',
                'email': 'johndoe@example.net',
                **kwargs,
            }
            response = self.client.post(self.__SIGNUP_PAGE_URL, data)
            return response


class TestSignup(BaseSignupTest.TestCase):
    """Test signing up a new user."""

    def test_user_can_access_signup_page(self):
        response = self._visit_signup()
        self.assertEqual(response.status_code, 200)

    def test_user_can_fill_signup_form(self):
        self._signup()
        self.assertTrue(User.objects.filter(username='johndoe').exists())

    def test_user_is_redirected_to_login_after_signup(self):
        response = self._signup()
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/accounts/login/')

    def test_email_is_required(self):
        response = self._signup(email=None)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='johndoe').exists())


class TestNonMatchingPasswordsSignup(BaseSignupTest.TestCase):
    """Test signing up with non-matching passwords."""

    def _signup(self, **kwargs):
        return super()._signup(password1='foo', password2='bar', **kwargs)

    def test_if_passwords_do_not_match_then_no_error(self):
        response = self._signup()
        self.assertEqual(response.status_code, 200)

    def test_if_passwords_do_not_match_then_user_not_created(self):
        self._signup(username='alice')
        self.assertFalse(User.objects.filter(username='alice').exists())
