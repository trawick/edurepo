from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    """ A teacher must be linked to a registered user.  The separate
    e-mail field here is how the public gets access to this teacher's
    classes, which may be a different e-mail address than is associated
    with the teacher's login (e.g., google id).
    """
    email = models.EmailField(primary_key=True, unique=True)
    # Why doesn't user have to be unique?  Same teacher with different
    # contact e-mails for different classes...
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' (public e-mail ' + self.email + ')'


class TeacherClass(models.Model):
    name = models.CharField(max_length=100)  # how this teacher refers to the class
    course_id = models.CharField(max_length=30)  # the short name of the standard class in the repo
    teacher = models.ForeignKey(Teacher)
    # XXX let the next field default to how we are currently running?
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
    comments = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return "Objective %s on %s for %s" % (self.objective, self.date, str(self.teacher_class))

    class Meta:
        verbose_name_plural = "entries"
