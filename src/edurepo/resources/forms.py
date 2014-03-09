from django import forms
from models import Resource


class ResourceForm(forms.ModelForm):

    objective = forms.CharField(label="Learning objective")
    url = forms.URLField(label="URL of resource")
    notes = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Resource
        fields = ('objective', 'url', 'notes')
