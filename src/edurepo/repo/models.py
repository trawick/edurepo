from django.core.validators import RegexValidator
from django.db import models
from core.utils import ellipsis

id_regex = '^[A-Za-z0-9-]*$'
objective_id_regex = '^[A-Za-z0-9-\.]*$'


class RepoLanguageField(models.CharField):

    # Use en, en-gb, etc. as in HTTP
    # Make sure that any language codes in the db match HTTP use
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('es', 'Spanish'),
    )

    description = "Language of educational material"

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.LANGUAGE_CHOICES
        kwargs['max_length'] = 8  # from HTTP
        kwargs['blank'] = True
        kwargs['default'] = 'en'
        super(RepoLanguageField, self).__init__(*args, **kwargs)


class CourseCategory(models.Model):
    """Broad category of courses, such as K-12 Science, K-12 Mathematics,
    etc."""
    id_desc = 'Course category ids may contain only letters, numbers, and hyphens.'
    id = models.CharField(max_length=8, primary_key=True, unique=True,
                          validators=[RegexValidator(regex=id_regex, message=id_desc)])
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.id + ' - ' + self.description

    class Meta:
        verbose_name_plural = "course categories"


class Course(models.Model):
    id_desc = 'Course ids may contain only letters, numbers, and hyphens.'
    id = models.CharField(max_length=30, primary_key=True, unique=True,
                          validators=[RegexValidator(regex=id_regex, message=id_desc)])
    cat = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=4000)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.id + '-' + ellipsis(self.description, 80)


class LearningObjective(models.Model):
    id_desc = 'Learning objective ids may contain only letters, numbers, hyphens, and periods.'
    id = models.CharField(max_length=40, primary_key=True, unique=True,
                          validators=[RegexValidator(regex=objective_id_regex, message=id_desc)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.CharField(max_length=4096)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.id + '-' + ellipsis(self.description, 60)


class ReferenceText(models.Model):
    learning_objective = models.OneToOneField(LearningObjective, primary_key=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=4000)
    language = RepoLanguageField()

    def __unicode__(self):
        return ellipsis(self.text, 60)


class ICan(models.Model):
    learning_objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    statement = models.CharField(max_length=200)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.statement


class MultipleChoiceItem(models.Model):
    learning_objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    language = RepoLanguageField()
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200, blank=True)
    choice4 = models.CharField(max_length=200, blank=True)
    choice5 = models.CharField(max_length=200, blank=True)
    MC_TYPE_CHOICES = (
        ('1', 'One of the provided answers is the only correct answer in the universe.'),
        ('2', 'Only one of the provided answers is correct, but there may be more correct answers in the universe.'),
        ('3', 'None of the provided answers is correct.'),
    )
    type = models.CharField(max_length=1, choices=MC_TYPE_CHOICES)
    ANS_CHOICES = (
        (1, 'The 1st answer is the correct choice.'),
        (2, 'The 2nd answer is the correct choice.'),
        (3, 'The 3rd answer is the correct choice.'),
        (4, 'The 4th answer is the correct choice.'),
        (5, 'The 5th answer is the correct choice.'),
    )
    ans = models.PositiveSmallIntegerField(choices=ANS_CHOICES)

    def __unicode__(self):
        return self.question


class GlossaryItem(models.Model):
    term = models.CharField(max_length=60)
    learning_objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    definition = models.CharField(max_length=4096)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.term + ' (' + ellipsis(self.definition, 60) + ')'

    class Meta:
        unique_together = ('term', 'learning_objective')


class TrueFalseItem(models.Model):
    learning_objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    statement = models.CharField(max_length=1024)
    answer = models.BooleanField(default=None)
    language = RepoLanguageField()

    def __unicode__(self):
        return "%s (%s)" % (self.statement, self.answer)
