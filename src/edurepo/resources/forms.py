from django import forms
from django.utils.translation import gettext as _
from models import Resource, ResourceSubmission


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ('objective', 'url', 'notes')
        labels = {'objective': _('Learning objective'),
                  'url': _('URL of resource')}
        widgets = {'notes': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
                   'url': forms.TextInput(attrs={'size': 80})}


class ResourceSubmissionForm(forms.ModelForm):

    type_choices = [('v', 'Up-vote'), ('f', 'Flag as inappropriate')]
    type = forms.ChoiceField(required=True, choices=type_choices)

    class Meta:
        model = ResourceSubmission
        fields = ('resource', 'type', 'comment')
        labels = {'comment': _('Optional written comments'),
                  'type': _('Type of comment')}
        widgets = {'comment': forms.Textarea(attrs={'cols': 80, 'rows': 2})}
