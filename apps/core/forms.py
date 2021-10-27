from django import forms

from apps.core.models import Media


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ("file",)
