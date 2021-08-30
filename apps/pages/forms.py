from django import forms
from apps.core.widgets import (
    CustomClearableFileInput,
    CustomDateInput,
    CustomDateTimeInput,
)


class SampleFile:
    url = "file.txt"

    def __str__(self) -> str:
        return self.url


class DesignSystemForm(forms.Form):
    """Form for the design system page."""

    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()
    date_of_birth = forms.DateField(widget=CustomDateInput)
    published_at = forms.DateTimeField(widget=CustomDateTimeInput)
    gender = forms.ChoiceField(choices=((1, "Male"), (2, "Female")))
    level = forms.ChoiceField(
        choices=((1, "Beginner"), (2, "Intermediate"), (3, "Advanced")),
        widget=forms.RadioSelect,
    )
    is_published = forms.BooleanField()
    profile_picture = forms.FileField(widget=CustomClearableFileInput)
    resume = forms.FileField(
        widget=CustomClearableFileInput,
        initial=SampleFile(),
        required=False,
    )
