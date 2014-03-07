from django.test import TestCase
from models import Course


class BasicTests(TestCase):

    def test_1(self):
        """Basic creation/update of Course and default language"""
        class_id = 'Class01'
        c1 = Course(id=class_id, description='desc1')
        self.assertEquals(c1.language, 'en')
        c1.save()

        desc2 = 'desc2'
        c2 = Course(id=class_id, description=desc2)
        c2.save()

        obj = Course.objects.get(id=class_id)
        self.assertEquals(obj.description, desc2)

        self.assertEquals(obj.language, 'en')
