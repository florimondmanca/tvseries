"""Test API endpoints to subscribe to shows."""
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from series.models import APIShow

User = get_user_model()


class SubscriptionTest:

    class TestCase(TestCase):

        def setUp(self):
            self.show = APIShow.objects.create(id=1402, title='Walking Dead')
            self.user = User.objects.create_user(
                username='johndoe',
                password='admin',
            )

        def _force_login(self):
            self.client.force_login(self.user)


class TestSubscribe(SubscriptionTest.TestCase):
    """Test subscribing to a show."""

    def _subscribe(self, pk=1402):
        return self.client.post(f'/subscribe/{pk}')

    def test_if_not_authenticated_then_unauthorized_with_json_error(self):
        response = self._subscribe()
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_if_not_subscribed_then_subscribed_after_call(self):
        self._force_login()
        response = self._subscribe()
        self.assertEqual(response.status_code, 200)
        show = APIShow.objects.get(pk=self.show.pk)
        self.assertTrue(show.followers.filter(pk=self.user.pk).exists())

    def test_if_show_does_not_exist_then_it_is_fetched_from_api(self):
        # TODO with a mock of the TMDB API
        pass


class TestUnsubscribe(SubscriptionTest.TestCase):
    """Test unsubscribing to a show."""

    def _unsubscribe(self, pk=1402):
        return self.client.delete(f'/subscribe/{pk}')

    def test_if_not_authenticated_then_unauthorized_with_json_error(self):
        response = self._unsubscribe()
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_if_subscribed_then_unsubscribed_after_call(self):
        self._force_login()
        response = self._unsubscribe()
        self.assertEqual(response.status_code, 200)
        show = APIShow.objects.get(pk=self.show.pk)
        self.assertFalse(show.followers.filter(pk=self.user.pk).exists())

    def test_if_show_does_not_exist_then_no_error(self):
        self._force_login()
        response = self._unsubscribe(pk=42)
        self.assertEqual(response.status_code, 200)
