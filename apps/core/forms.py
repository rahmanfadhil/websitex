from typing import Optional

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class CrispyFormMixin:
    """
    Add a crispy form helper which disables automatic csrf and form tag.
    """

    submit_label: Optional[str] = None

    def get_submit_button(self) -> Submit:
        """Get the submit button for the form."""
        return Submit("save", self.get_submit_label(), css_class="mt-2")

    def get_submit_label(self) -> str:
        """Get the submit button text for the form."""
        if self.submit_label:
            return self.submit_label
        elif hasattr(self, "instance"):
            return "Create" if self.instance.pk is None else "Save changes"
        else:
            return "Submit"

    def get_layout(self) -> Optional[Layout]:
        """Define a custom crispy forms layout."""
        return None

    @property
    def helper(self) -> FormHelper:
        helper = FormHelper()
        helper.layout = self.get_layout()
        helper.add_input(self.get_submit_button())
        return helper
