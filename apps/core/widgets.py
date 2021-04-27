from django import forms
from django.utils.html import format_html


class TrixEditorInput(forms.HiddenInput):
    """
    Use Basecamp's Trix rich text editor for your TextField.
    """

    def render(self, name, value, attrs, renderer):
        trix_element = format_html(
            '<trix-editor input="{}"></trix-editor>', attrs["id"]
        )
        return super().render(name, value, attrs, renderer) + trix_element


class MoneyInput(forms.TextInput):
    """
    Format money in text input, can be used in DecimalField.
    """

    pass


class TagsInput(forms.TextInput):
    """
    Use multiple tags input (@yaireo/tagify).
    """

    pass
