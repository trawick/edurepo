from django.contrib import admin

from resources.models import Resource, ResourceSubmission, ResourceVerification

admin.site.register(Resource)
admin.site.register(ResourceSubmission)
admin.site.register(ResourceVerification)
