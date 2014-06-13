import os
import unittest
from django.test import TestCase
from utils import description_for_objective, ellipsis, objectives_for_course


class BasicTests(TestCase):

    def test_ellipsis(self):
        long_str = 'yadayadayada'
        self.assertEquals(ellipsis(long_str, 5), 'ya...')
        self.assertEquals(ellipsis(long_str, len(long_str) - 1), long_str[:-4] + '...')
        self.assertEquals(ellipsis(long_str, len(long_str) + 1), long_str)
        self.assertEquals(ellipsis(long_str, 100), long_str)

    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_objective_lookup(self):
        desc = description_for_objective('MG4-FACTMULT', os.environ['TEST_PROVIDER'])
        self.assertTrue('factors and multiples' in desc)

    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_course_lookup(self):
        res = objectives_for_course('MG4', os.environ['TEST_PROVIDER'])
        self.assertTrue('MG4-FACTMULT' in [y for (y, z) in res])
