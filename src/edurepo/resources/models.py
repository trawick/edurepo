from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from urlparse import urlparse


def validate_resource_url(u):
    o = urlparse(u)
    if o.scheme not in ['http', 'https']:
        raise ValidationError(u'"%s" is not a supported URL scheme' % o.scheme)
    if len(o.path) < 1 or o.path[0] != '/':
        raise ValidationError(u'"%s" is not a supported URL path' % o.path)
    if len(o.netloc) < 1 or ':' in o.netloc or '@' in o.netloc:
        raise ValidationError(u'"%s" is not a supported network address' % o.netloc)


class Resource(models.Model):
    objective = models.CharField(max_length=40)
    votes = models.IntegerField(default=0)
    inappropriate_flags = models.IntegerField(default=0)
    url = models.URLField(validators=[validate_resource_url])
    notes = models.CharField(max_length=1000, blank=True)
    when_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Resource for %s: %s" % (self.objective, self.url)

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

    def clean(self):
        super(ResourceSubmission, self).clean()
        if self.type is 'v':
            created = ResourceSubmission.objects.get(user=self.user, resource=self.resource, type='c')
            if created:
                raise ValidationError('You cannot vote on a resource you submitted.')

    def __unicode__(self):
        return "%s/%s/%s" % (self.user, self.resource, self.type)

    class Meta:
        unique_together = ('user', 'resource', 'type')
