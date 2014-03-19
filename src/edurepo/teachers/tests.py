import os
import unittest

from django.core.exceptions import ValidationError
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from models import Teacher, TeacherClass


class BasicTests(LiveServerTestCase):

    def setUp(self):
        self.email1 = 'trawick@example.com'
        self.name1 = 'Jeff T'

        self.u1 = User.objects.create_user(username='user1', email='user1@example.com')
        self.t1 = Teacher(email=self.email1, name=self.name1, user=self.u1)
        self.t1.save()

        if 'TEST_PROVIDER' in os.environ:
            self.good_provider = os.environ['TEST_PROVIDER']
        else:
            # This is the default server thread started by django test,
            # but it only works for this app.
            self.good_provider = 'http://localhost:8081/'  # default
        self.bad_provider = 'http://127.0.0.1:65535/'

        self.good_course = 'MG4'
        self.bad_course = 'xxx' + self.good_course + 'xxx'

    def test_1(self):
        """Basic creation/update of Teacher"""
        email = 'trawick@example.com'
        name1 = 'Jeff'
        name2 = 'Jeff T'
        t1 = Teacher(email=email, name=name1, user=self.u1)
        t1.save()
        t2 = Teacher(email=email, name=name2, user=self.u1)
        t2.save()

        obj = Teacher.objects.get(email=email)
        self.assertEquals(obj.name, name2)

    # This test case requires a working API provider, including
    # the repo API.  That won't work when using the server thread
    # started by django test.
    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_good_repo_and_course_id(self):
        tc = TeacherClass(name='1st period math (TGRC)',
                          course_id=self.good_course, teacher=self.t1,
                          repo_provider=self.good_provider)
        tc.full_clean()
        tc.save()

    def test_good_repo_and_bad_course_id(self):
        tc = TeacherClass(name='1st period math (TGRBC)',
                          course_id=self.bad_course, teacher=self.t1,
                          repo_provider=self.good_provider)
        self.assertRaises(ValidationError, lambda: tc.full_clean())

    def test_bad_repo_and_good_course_id(self):
        tc = TeacherClass(name='1st period math (TBRGC)',
                          course_id=self.good_course, teacher=self.t1,
                          repo_provider=self.bad_provider)
        self.assertRaises(ValidationError, lambda: tc.full_clean())
