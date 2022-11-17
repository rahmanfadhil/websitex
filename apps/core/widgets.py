from django import forms


class CustomDateInput(forms.DateInput):
    input_type = "date"


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = "widgets/clearable_file_input.html"


class CustomFileInput(forms.FileInput):
    template_name = "widgets/clearable_file_input.html"


class CustomDateTimeInput(forms.DateTimeInput):
    """
    Not supported in Firefox yet. So, we added a placeholder to let the users
    know how to format the date and time.

    https://caniuse.com/mdn-html_elements_input_input-datetime-local
    """

    input_type = "datetime-local"

    def build_attrs(self, base_attrs, extra_attrs):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.setdefault("placeholder", "yyyy-mm-dd hh:mm:ss")
        return attrs
