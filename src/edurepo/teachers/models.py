from django.db import models


class Teacher(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' (' + self.email + ')'


class TeacherClass(models.Model):
    name = models.CharField(max_length=100)  # how this teacher refers to the class
    course_id = models.CharField(max_length=30)  # the short name of the standard class in the repo
    teacher = models.ForeignKey(Teacher)
    repo_provider = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name + '(' + self.course_id + ') taught by ' + str(self.teacher)

    class Meta:
        verbose_name_plural = "classes"


class Entry(models.Model):
    teacher = models.ForeignKey(Teacher)
    teacher_class = models.ForeignKey(TeacherClass)
    date = models.DateField(blank=False)
    objective = models.CharField(max_length=40)

    def __unicode__(self):
        return "Objective %s on %s for %s" % (self.objective, self.date, str(self.teacher_class))

    class Meta:
        verbose_name_plural = "entries"
