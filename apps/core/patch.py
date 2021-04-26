from http import HTTPStatus

from django.views.generic.edit import FormMixin

old_form_invalid = FormMixin.form_invalid


def form_invalid(self, form):
    """
    Change the default behavior of the FormMixin.form_invalid method. If the
    form is invalid, render the invalid form with 422 status code.
    """
    response = old_form_invalid(self, form)
    response.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    return response


FormMixin.form_invalid = form_invalid
