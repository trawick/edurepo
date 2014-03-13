from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from urlparse import urlparse
from repo.models import LearningObjective


def validate_resource_url(u):
    o = urlparse(u)
    if o.scheme not in ['http', 'https']:
        raise ValidationError(u'"%s" is not a supported URL scheme' % o.scheme)
    if len(o.path) < 1 or o.path[0] != '/':
        raise ValidationError(u'"%s" is not a supported URL path' % o.path)
    if len(o.netloc) < 1 or ':' in o.netloc or '@' in o.netloc:
        raise ValidationError(u'"%s" is not a supported network address' % o.netloc)


class Resource(models.Model):
    objective = models.ForeignKey(LearningObjective)
    votes = models.IntegerField(default=0)
    inappropriate_flags = models.IntegerField(default=0)
    url = models.URLField(validators=[validate_resource_url])
    notes = models.CharField(max_length=1000, blank=True)
    when_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Resource for %s: %s" % (self.objective.id, self.url)

    class Meta:
        unique_together = ('objective', 'url')


class ResourceSubmission(models.Model):
    user = models.ForeignKey(User)
    resource = models.ForeignKey(Resource)
    RS_TYPE_CHOICES = (
        ('c', 'Creator'),
        ('v', 'Voter'),
        ('f', 'Flagger'),
    )
    type = models.CharField(max_length=1, choices=RS_TYPE_CHOICES, default='c')
    comment = models.CharField(max_length=160, blank=True)
    when = models.DateTimeField(auto_now_add=True)

    verbs = {'c': 'created', 'v': 'voted on', 'f': 'flagged'}

    def clean(self):
        super(ResourceSubmission, self).clean()
        if self.type is 'v':
            created = ResourceSubmission.objects.filter(user=self.user, resource=self.resource, type='c')
            if len(created) > 0:  # should be 1
                raise ValidationError('You cannot vote on a resource you submitted.')

    def __unicode__(self):
        return "%s %s %s" % (self.user, ResourceSubmission.verbs[str(self.type)], self.resource)

    class Meta:
        unique_together = ('user', 'resource', 'type')


class ResourceVerification(models.Model):
    url = models.URLField(primary_key=True, unique=True)
    last_success = models.DateTimeField(blank=True, null=True)
    last_failure = models.DateTimeField(blank=True, null=True)
    document_title = models.CharField(max_length=120, blank=True)

    def __unicode__(self):
        valid = 'Valid'
        invalid = 'Invalid'
        if not self.last_success:
            status = invalid
        elif not self.last_failure:
            status = valid
        elif self.last_success > self.last_failure:
            status = valid
        else:
            status = invalid
        return status + ':' + self.url
