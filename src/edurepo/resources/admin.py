from django.contrib import admin
from django.db.models import F

from resources.models import Resource, ResourceSubmission, ResourceVerification


class ResourceAdmin(admin.ModelAdmin):
    search_fields = ('url',)

admin.site.register(Resource, ResourceAdmin)


class ResourceSubmissionAdmin(admin.ModelAdmin):
    search_fields = ('resource__url',)

admin.site.register(ResourceSubmission, ResourceSubmissionAdmin)


class UnreachableResourceFilter(admin.SimpleListFilter):
    title = 'unreachable resource'
    parameter_name = 'unreachable'

    def lookups(self, request, model_admin):
        return (
            ('unreachable', 'all unreachable'),
        )

    def queryset(self, request, queryset):
        if self.value():  # must be 'unreachable', since that's the only lookup option
            return queryset.exclude(last_success__gt=F('last_failure'))
        else:
            return queryset


class ResourceVerificationAdmin(admin.ModelAdmin):
    search_fields = ('url',)
    list_filter = (UnreachableResourceFilter,)

admin.site.register(ResourceVerification, ResourceVerificationAdmin)
