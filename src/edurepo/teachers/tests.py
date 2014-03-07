from django.test import TestCase
from models import Teacher


class BasicTests(TestCase):

    def test_1(self):
        """Basic creation/update of Teacher"""
        email = 'trawick@example.com'
        name1 = 'Jeff'
        name2 = 'Jeff T'
        t1 = Teacher(email=email, name=name1)
        t1.save()
        t2 = Teacher(email=email, name=name2)
        t2.save()

        obj = Teacher.objects.get(email=email)
        self.assertEquals(obj.name, name2)
