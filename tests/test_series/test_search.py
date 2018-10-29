from django.test import TestCase, override_settings


@override_settings(TMDB_CLIENT='tmdb.mock.MockTMDBClient')
class SearchShowsTest(TestCase):
    """Test searching for shows."""

    def test_search_shows(self):
        response = self.client.get('/search/walking')
        self.assertEqual(response.status_code, 200)
