import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from models import Resource


class BasicTests(TestCase):

    def test_1(self):
        """Basic creation of Resource, disallowing same URL+objective combination"""
        lo1 = 'Obj01'
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
            r = Resource(objective='TBUObj' + str(i), url=bad_url)
            self.assertRaises(ValidationError, lambda: r.full_clean())
