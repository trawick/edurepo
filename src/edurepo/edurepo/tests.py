from django.test import TestCase


class BasicTests(TestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertContains(response, 'Edjective.org reference views', status_code=200, html=False)
