import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import requests

logger = logging.getLogger(__name__)


class Teacher(models.Model):
    """ A teacher must be linked to a registered user.  The separate
    e-mail field here is how the public gets access to this teacher's
    classes, which may be a different e-mail address than is associated
    with the teacher's login (e.g., google id).
    """
    email = models.EmailField(primary_key=True, unique=True)
    # Why doesn't user have to be unique?  Same teacher with different
    # contact e-mails for different classes...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' (public e-mail ' + self.email + ')'


class TeacherClass(models.Model):
    name = models.CharField(max_length=100)  # how this teacher refers to the class
    course_id = models.CharField(max_length=30)  # the short name of the standard class in the repo
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # A default for this is provided in the add_class form
    repo_provider = models.CharField(max_length=250)

    def clean(self):
        super(TeacherClass, self).clean()
        if not self.repo_provider:
            # This field is required.  Let the normal validation error bubble up
            # instead of tripping here.
            return
        bad_repo_msg = 'The repository is unavailable or the repository URL is invalid.'
        bad_course_id_msg = 'The course id is invalid'
        class_url = self.repo_provider + 'repo/api/course/' + self.course_id + '/'
        try:
            logger.info("Fetching %s" % class_url)
            response = requests.get(class_url, timeout=5)
        except requests.exceptions.ConnectionError:
            logger.exception("Error retrieving %s" % class_url)
            raise ValidationError(bad_repo_msg + ' (Connection error)')
        # temporary hack for https://github.com/kennethreitz/requests/issues/2192
        except requests.packages.urllib3.exceptions.ProtocolError:
            logger.exception("Error retrieving %s" % class_url)
            raise ValidationError(bad_repo_msg + ' (Connection error)')

        if response.status_code == 404:
            raise ValidationError(bad_course_id_msg + ' (404 error from ' + class_url + ')')
        elif response.status_code != 200:
            raise ValidationError(bad_repo_msg + ' (HTTP error ' + response.status_code + ')')

    def __unicode__(self):
        return self.name + '(' + self.course_id + ') taught by ' + str(self.teacher)

    class Meta:
        verbose_name_plural = "classes"
        unique_together = ('name', 'teacher')


class Entry(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    teacher_class = models.ForeignKey(TeacherClass, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    objective = models.CharField(max_length=40)
    comments = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return "Objective %s on %s for %s" % (self.objective, self.date, str(self.teacher_class))

    class Meta:
        verbose_name_plural = "entries"
        unique_together = ('teacher_class', 'date', 'objective')
