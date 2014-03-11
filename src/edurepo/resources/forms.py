from django import forms
from django.utils.translation import gettext as _
from models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ('objective', 'url', 'notes')
        labels = {'objective': _('Learning objective'),
                  'url': _('URL of resource')}
        widgets = {'notes': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
                   'url': forms.TextInput(attrs={'size': 80})}
