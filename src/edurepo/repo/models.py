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
        super(RepoLanguageField, self).__init__(*args, **kwargs)


class Course(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    description = models.CharField(max_length=200)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.id


class LearningObjective(models.Model):
    id = models.CharField(max_length=40, primary_key=True, unique=True)
    course = models.ForeignKey(Course)
    formal_description = models.CharField(max_length=4096)
    simple_description = models.CharField(max_length=4096)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.id


class ICan(models.Model):
    learning_objective = models.ForeignKey(LearningObjective)
    statement = models.CharField(max_length=200)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.statement


class GlossaryItem(models.Model):
    term = models.CharField(max_length=60)
    learning_objective = models.ForeignKey(LearningObjective)
    definition = models.CharField(max_length=4096)
    language = RepoLanguageField()

    def __unicode__(self):
        return self.term


class TrueFalseItem(models.Model):
    learning_objective = models.ForeignKey(LearningObjective)
    statement = models.CharField(max_length=1024)
    answer = models.BooleanField()
    language = RepoLanguageField()

    def __unicode__(self):
        return "%s (%s)" % (self.statement, self.answer)
