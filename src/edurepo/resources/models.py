from django.db import models


class Resource(models.Model):
    objective = models.CharField(max_length=40)
    votes = models.IntegerField()
    inappropriate_flags = models.IntegerField()
    url = models.CharField(max_length=250)
    notes = models.CharField(max_length=1000, blank=True)
    when_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Resource for %s: %s" % (self.objective, self.url)


class ResourceSubmission(models.Model):
    email = models.EmailField(unique=False)
    resource = models.ForeignKey(Resource)
    RS_TYPE_CHOICES = (
        ('c', 'Creator'),
        ('v', 'Voter'),
        ('f', 'Flagger'),
    )
    type = models.CharField(max_length=1, choices=RS_TYPE_CHOICES)

    def __unicode__(self):
        return "%s/%s/%s" % (self.email, self.resource, self.type)
