from django.test import TestCase
from utils import ellipsis


class BasicTests(TestCase):

    def test_ellipsis(self):
        long_str = 'yadayadayada'
        self.assertEquals(ellipsis(long_str, 5), 'ya...')
        self.assertEquals(ellipsis(long_str, len(long_str) - 1), long_str[:-4] + '...')
        self.assertEquals(ellipsis(long_str, len(long_str) + 1), long_str)
        self.assertEquals(ellipsis(long_str, 100), long_str)
