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
    objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    inappropriate_flags = models.IntegerField(default=0)
    url = models.URLField(validators=[validate_resource_url])
    notes = models.CharField(max_length=1000, blank=True)
    when_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Resource %d for %s: %s" % (self.id, self.objective.id, self.url)

    class Meta:
        unique_together = ('objective', 'url')


class ResourceSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    RS_TYPE_CHOICES = (
        ('c', 'Creator'),
        ('v', 'Voter'),
        ('f', 'Flagger'),
    )
    type = models.CharField(max_length=1, choices=RS_TYPE_CHOICES, default='c')
    comment = models.CharField(max_length=160, blank=True)
    when = models.DateTimeField(auto_now_add=True, editable=False)

    verbs = {'c': 'created', 'v': 'voted on', 'f': 'flagged'}

    def type_str(self):
        if self.type == 'c':
            return 'Created'
        if self.type == 'v':
            return 'Up-voted'
        if self.type == 'f':
            return 'Inappropriate'
        return 'unknown-type'

    def clean(self):
        super(ResourceSubmission, self).clean()
        if self.type is 'v':
            created = ResourceSubmission.objects.filter(user=self.user, resource=self.resource, type='c')
            if len(created) > 0:  # should be 1
                raise ValidationError('You cannot vote on a resource you submitted.')
        # The unique_together constraint is enforced at the database layer,
        # but not at the form layer (since user is not part of the form).
        # Check that manually so that we get an error message on the form.
        #duplicate = ResourceSubmission.objects.filter(user=self.user, resource=self.resource, type=self.type)
        #if len(duplicate) > 0:
        #    if self.type is 'v':
        #        raise ValidationError('You already voted once for this resource.')
        #    elif self.type is 'f':
        #        raise ValidationError('You already flagged this resource once.')
        #    else:
        #        # should-not-occur; let it blow up at the database layer
        #        pass

    def __unicode__(self):
        return "%s %s %s" % (self.user, ResourceSubmission.verbs[str(self.type)], self.resource)

    class Meta:
        unique_together = ('user', 'resource', 'type')


class ResourceVerification(models.Model):
    url = models.URLField(primary_key=True, unique=True)
    last_success = models.DateTimeField(blank=True, null=True)
    last_failure = models.DateTimeField(blank=True, null=True)
    document_title = models.CharField(max_length=120, blank=True)
    # just the type, not the charset
    content_type = models.CharField(max_length=127, blank=True)

    def status_char(self):
        valid = 'V'
        invalid = 'I'
        if not self.last_success:
            status = invalid
        elif not self.last_failure:
            status = valid
        elif self.last_success > self.last_failure:
            status = valid
        else:
            status = invalid
        return status

    def status_str(self):
        s = self.status_char()
        if s == 'V':
            return 'Valid'
        else:
            return 'Invalid'

    def __unicode__(self):
        return self.status_str() + ':' + self.url
