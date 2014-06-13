import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from models import Resource, ResourceSubmission
from repo.models import Course, CourseCategory, LearningObjective


class BasicTests(TestCase):

    def setUp(self):
        self.u1_password = 'F00LI5H'
        self.u1 = User.objects.create_user(username='user1', email='user1@example.com',
                                           password=self.u1_password)
        user = authenticate(username=self.u1.username, password=self.u1_password)
        assert user
        self.u2 = User.objects.create_user(username='user2', email='user2@example.com')
        self.cc0 = CourseCategory(id='TESTNA', description='Test Non-Academic')
        self.cc0.full_clean()
        self.cc0.save()
        self.c0 = Course(id='Class00', cat=self.cc0, description='Class00Desc')
        self.c0.full_clean()
        self.c0.save()
        self.lo0 = LearningObjective(id='C00LO00', course=self.c0, description='Dummy objective')
        self.lo0.full_clean()
        self.lo0.save()
        self.res1 = Resource(objective=self.lo0, url='http://www.example.com/XXX')
        self.res1.full_clean()
        self.res1.save()

    def test_1(self):
        """Basic creation of Resource, disallowing same URL+objective combination"""
        lo1 = self.lo0
        url1 = 'http://127.0.0.1/foo.html'
        r1 = Resource(objective=lo1, url=url1)
        self.assertEquals(r1.votes, 0)
        self.assertEquals(r1.inappropriate_flags, 0)
        r1.save()
        when_added = r1.when_added
        now = datetime.datetime.now()
        when_added = when_added.replace(tzinfo=None)
        self.assertTrue(now - when_added < datetime.timedelta(seconds=5))

        r2 = Resource(objective=lo1, url=url1)
        self.assertRaises(IntegrityError, lambda: r2.save())

    def test_bad_url(self):
        bad_urls = ('ftp://trawick:private@example.com/',
                    'http://trawick:private@example.com/',
                    )
        for (bad_url, i) in zip(bad_urls, range(len(bad_urls))):
            r = Resource(objective=self.lo0, url=bad_url)
            self.assertRaises(ValidationError, lambda: r.full_clean())

    def test_duplicate_submission(self):
        lo1 = self.lo0
        url = 'http://www.google.com/'
        r = Resource(objective=lo1, url=url)
        r.full_clean()
        r.save()

        rs = ResourceSubmission(user=self.u1, resource=r, type='c')
        rs.full_clean()
        rs.save()

        rs = ResourceSubmission(user=self.u1, resource=r, type='c')
        self.assertRaises(ValidationError, lambda: rs.full_clean())

        # can't vote on a resource you submitted
        rs = ResourceSubmission(user=self.u1, resource=r, type='v')

        with self.assertRaisesRegexp(ValidationError, 'cannot vote.*submitted'):
            rs.full_clean()

        # okay to flag a resource you submitted as inappropriate

    def test_strings(self):
        lo2 = self.lo0
        url = 'http://www.google.com/'
        r = Resource(objective=lo2, url=url)
        r.full_clean()
        r.save()

        rs = ResourceSubmission(user=self.u1, resource=r, type='c')
        rs.full_clean()
        rs.save()

        self.assertTrue(' created ' in str(rs))

        rs = ResourceSubmission(user=self.u1, resource=r, type='f')
        rs.full_clean()
        rs.save()

        self.assertTrue(' flagged ' in str(rs))

        rs = ResourceSubmission(user=self.u2, resource=r, type='v')
        rs.full_clean()
        rs.save()

        self.assertTrue(' voted on ' in str(rs))

    def test_index(self):
        response = self.client.get("/resources/")
        self.assertContains(response, self.res1.url, status_code=200, html=False)

    def test_detail(self):
        detail_url = "/resources/" + str(self.res1.id) + "/"
        response = self.client.get(detail_url)
        self.assertContains(response, self.res1.url, status_code=200, html=False)

    def test_create_resource(self):
        login = self.client.login(username=self.u1.username, password=self.u1_password)
        self.assertTrue(login)
        create_url = '/resources/create/?objective=C00LO00'
        response = self.client.get(create_url, follow=True)
        self.assertContains(response, 'Submit a resource', status_code=200)
        self.assertContains(response, 'C00LO00')
        response = self.client.post(create_url, {'url': 'http://www.example.com/',
                                                 'objective': 'C00LO00'}, follow=True)
        self.assertNotContains(response, 'form-group has-error')
        self.assertContains(response, 'http://www.example.com/', status_code=200)
        self.assertContains(response, 'C00LO00')

    def test_comment_on_resource(self):
        login = self.client.login(username=self.u1.username, password=self.u1_password)
        self.assertTrue(login)
        comment_url = "/resources/" + str(self.res1.id) + "/comment/"
        response = self.client.get(comment_url, follow=True)
        self.assertContains(response, 'Comment on a resource', status_code=200)
        self.assertContains(response, self.res1.url)
        response = self.client.post(comment_url, {'resource': str(self.res1.id),
                                                  'type': 'v'}, follow=True)
        self.assertNotContains(response, 'form-group has-error')
