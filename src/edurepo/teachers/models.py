from django.db import models


class Teacher(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ForeignKey(Teacher)

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    teacher = models.ForeignKey(Teacher)
    course = models.ForeignKey(Course)
    date = models.DateField(blank=False)
    objective = models.CharField(max_length=40)

    def __unicode__(self):
        return "Objective %s on %s" % (self.objective, self.date)

    class Meta:
        verbose_name_plural = "entries"
