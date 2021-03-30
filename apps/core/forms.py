from typing import Optional
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CrispyFormMixin:
    """
    Add a crispy form helper which disables automatic csrf and form tag.
    """

    submit_label: Optional[str] = None

    def get_submit_label(self) -> str:
        if self.submit_label:
            return self.submit_label
        elif hasattr(self, "instance"):
            return "Create" if self.instance.pk is None else "Save changes"
        else:
            return "Submit"

    @property
    def helper(self):
        helper = FormHelper()
        helper.add_input(Submit("save", self.get_submit_label(), css_class="mt-2"))
        return helper
