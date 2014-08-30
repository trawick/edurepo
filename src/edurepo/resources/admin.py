from django.contrib import admin
from django.db.models import F

from resources.models import Resource, ResourceSubmission, ResourceVerification


class ResourceAdmin(admin.ModelAdmin):
    search_fields = ('url',)

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceSubmission)


class UnreachableResourceFilter(admin.SimpleListFilter):
    title = 'unreachable resource'
    parameter_name = 'unreachable'

    def lookups(self, request, model_admin):
        return (
            ('unreachable', 'all unreachable'),
        )

    def queryset(self, request, queryset):
        if self.value():  # must be 'unreachable', since that's the only lookup option
            return queryset.filter(last_failure__gt=F('last_success'))
        else:
            return queryset


class ResourceVerificationAdmin(admin.ModelAdmin):
    list_filter = (UnreachableResourceFilter,)

admin.site.register(ResourceVerification, ResourceVerificationAdmin)
