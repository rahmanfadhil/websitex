from django import forms


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = "widgets/customclearablefileinput.html"


class CustomDateInput(forms.DateInput):
    input_type = "date"
