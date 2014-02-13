from django.db import models


class Course(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.id


class LearningObjective(models.Model):
    id = models.CharField(max_length=40, primary_key=True, unique=True)
    course = models.ForeignKey(Course)
    formal_description = models.CharField(max_length=4096)
    simple_description = models.CharField(max_length=4096)

    def __unicode__(self):
        return self.id


class GlossaryItem(models.Model):
    term = models.CharField(max_length=60)
    learning_objective = models.ForeignKey(LearningObjective)
    definition = models.CharField(max_length=4096)

    def __unicode__(self):
        return self.term


class TrueFalseItem(models.Model):
    learning_objective = models.ForeignKey(LearningObjective)
    statement = models.CharField(max_length=1024)
    answer = models.BooleanField()
