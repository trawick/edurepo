from django.db import models


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


class Course(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    description = models.CharField(max_length=4000)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.id + '-' + self.description


class LearningObjective(models.Model):
    id = models.CharField(max_length=40, primary_key=True, unique=True)
    course = models.ForeignKey(Course)
    formal_description = models.CharField(max_length=4096)
    simple_description = models.CharField(max_length=4096)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.id + '-' + self.formal_description[:60]


class ReferenceText(models.Model):
    learning_objective = models.ForeignKey(LearningObjective)
    text = models.CharField(max_length=4000)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.text[:60]


class ICan(models.Model):
    learning_objective = models.ForeignKey(LearningObjective)
    statement = models.CharField(max_length=200)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.statement


class MultipleChoiceItem(models.Model):
    learning_objective = models.ForeignKey(LearningObjective)
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
    learning_objective = models.ForeignKey(LearningObjective)
    definition = models.CharField(max_length=4096)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.term + ' (' + self.definition[:60] + ')'


class TrueFalseItem(models.Model):
    learning_objective = models.ForeignKey(LearningObjective)
    statement = models.CharField(max_length=1024)
    answer = models.BooleanField()
    language = RepoLanguageField()

    def __unicode__(self):
        return "%s (%s)" % (self.statement, self.answer)
