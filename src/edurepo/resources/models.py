from django.db import models


class Resource(models.Model):
    objective = models.CharField(max_length=40)
    votes = models.IntegerField()
    url = models.CharField(max_length=250)
    notes = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return "Resource for %s: %s" % (self.objective, self.url)