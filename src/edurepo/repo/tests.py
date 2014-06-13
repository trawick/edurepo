from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError, transaction
from django.test import TestCase
from models import Course, CourseCategory, GlossaryItem, LearningObjective, MultipleChoiceItem


class BasicTests(TestCase):

    def setUp(self):
        self.cc0 = CourseCategory(id='TESTNA', description='Test Non-Academic')
        self.cc0.full_clean()
        self.cc0.save()
        self.c0 = Course(id='Class00', cat=self.cc0, description='Class00Desc')
        self.c0.full_clean()
        self.c0.save()
        self.lo0 = LearningObjective(id='C00LO00', course=self.c0, description='XX_C00LO00_XX')
        self.lo0.full_clean()
        self.lo0.save()
        self.lo1 = LearningObjective(id='c00LO01', course=self.c0, description='XX_c00LO01_XX')
        self.lo1.full_clean()
        self.lo1.save()

    def test_1(self):
        """Basic creation/update of Course and default language"""
        class_id = 'Class01'
        c1 = Course(id=class_id, cat=self.cc0, description='desc1')
        self.assertEquals(c1.language, 'en')
        c1.save()

        desc2 = 'desc2'
        c2 = Course(id=class_id, cat=self.cc0, description=desc2)
        c2.save()

        obj = Course.objects.get(id=class_id)
        self.assertEquals(obj.description, desc2)

        self.assertEquals(obj.language, 'en')

    def test_duplicate_glossary_item(self):
        gi1 = GlossaryItem(term='term01', learning_objective=self.lo0)
        gi1.save()

        gi2 = GlossaryItem(term='term01', learning_objective=self.lo0)
        self.assertRaises(IntegrityError, lambda: gi2.save())

    def test_id_syntax(self):
        with self.assertRaises(DataError):
            with transaction.atomic():
                tis_cc0 = CourseCategory(id='123456789', description='too long')
                tis_cc0.save()

        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tis_cc1 = CourseCategory(id='has spc', description='will not work')
                tis_cc1.full_clean()

        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tis_c0 = Course(id='has space', cat=self.cc0, description='who cares')
                tis_c0.full_clean()

        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tis_lo0 = LearningObjective(id='has space', course=self.c0, description='foobar')
                tis_lo0.full_clean()

    def test_multiple_choice_constraints(self):
        tmcc_1 = MultipleChoiceItem(learning_objective=self.lo0,
                                    question='ABC?',
                                    choice1='xxx',
                                    choice2='yyy',
                                    type=1,
                                    ans=1)
        tmcc_1.full_clean()
        self.assertEqual(tmcc_1.language, 'en', 'Language did not default to "en"')

        # bad value for type
        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tmcc_2 = MultipleChoiceItem(learning_objective=self.lo0,
                                            question='ABC?',
                                            choice1='xxx',
                                            choice2='yyy',
                                            type=7,
                                            ans=1)
                tmcc_2.full_clean()

        # question too long
        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tmcc_3 = MultipleChoiceItem(learning_objective=self.lo0,
                                            question='1' * 401,
                                            choice1='xxx',
                                            choice2='yyy',
                                            type=7,
                                            ans=1)
                tmcc_3.full_clean()

    def test_index(self):
        response = self.client.get("/repo/")
        self.assertContains(response, 'Class00', status_code=200, html=False)

    def test_detail(self):
        response = self.client.get("/repo/Class00/")
        self.assertContains(response, 'C00LO00', status_code=200, html=False)

    def test_by_objective(self):
        response = self.client.get("/repo/Class00/C00LO00/")
        self.assertContains(response, 'XX_C00LO00_XX', status_code=200, html=False)
