from django.db import IntegrityError
from django.test import TestCase
from models import Course, GlossaryItem, LearningObjective


class BasicTests(TestCase):

    def setUp(self):
        self.c0 = Course(id='Class00', description='Class00Desc')
        self.c0.save()
        self.lo0 = LearningObjective(id='C00LO00', course=self.c0)
        self.lo0.save()
        self.lo1 = LearningObjective(id='c00LO01', course=self.c0)
        self.lo1.save()

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

    def test_duplicate_glossary_item(self):
        gi1 = GlossaryItem(term='term01', learning_objective=self.lo0)
        gi1.save()

        gi2 = GlossaryItem(term='term01', learning_objective=self.lo0)
        self.assertRaises(IntegrityError, lambda: gi2.save())
