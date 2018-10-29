from django.test import TestCase, override_settings


@override_settings(TMDB_CLIENT='tmdb.mock.MockTMDBClient')
class SearchShowsTest(TestCase):
    """Test searching for shows."""

    def test_can_access_search_page(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_perform_search_redirects_to_search_results_page(self):
        response = self.client.post('/search/', {'search_term': 'walking'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/search/walking')

    def test_access_search_results(self):
        response = self.client.get('/search/walking')
        self.assertEqual(response.status_code, 200)
