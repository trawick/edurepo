import urllib2

from django.core.exceptions import ValidationError
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
    # A default for this is provided in the add_class form
    repo_provider = models.CharField(max_length=250)

    def clean(self):
        super(TeacherClass, self).clean()
        bad_repo_msg = 'The repository is unavailable or the repository URL is invalid.'
        bad_course_id_msg = 'The course id is invalid'
        try:
            class_url = self.repo_provider + 'repo/api/course/' + self.course_id + '/'
            req = urllib2.Request(url=class_url)
            rsp = urllib2.urlopen(req, timeout=5)
        except urllib2.HTTPError as e:
            if e.code == 404:
                raise ValidationError(bad_course_id_msg + ' (404 error from ' + class_url + ')')
            else:
                raise ValidationError(bad_repo_msg + ' (HTTPError ' + e.code + ')')
        except urllib2.URLError:
            raise ValidationError(bad_repo_msg + ' (URLError)')
        finally:
            try:
                rsp.close()
            except NameError:
                pass

    def __unicode__(self):
        return self.name + '(' + self.course_id + ') taught by ' + str(self.teacher)

    class Meta:
        verbose_name_plural = "classes"
        unique_together = ('name', 'teacher')


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
        unique_together = ('teacher_class', 'date', 'objective')
