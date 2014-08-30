from django.contrib import admin

from resources.models import Resource, ResourceSubmission, ResourceVerification

class ResourceAdmin(admin.ModelAdmin):
    search_fields = ('url',)

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceSubmission)
admin.site.register(ResourceVerification)
