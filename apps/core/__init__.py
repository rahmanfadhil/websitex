from http import HTTPStatus

from django.views.generic.edit import FormMixin

old_form_valid = FormMixin.form_valid
old_form_invalid = FormMixin.form_invalid


def form_valid(self, form):
    """
    Ensures response has 303 status on when the form was valid.
    """
    response = old_form_valid(self, form)
    response.status_code = HTTPStatus.SEE_OTHER
    return response


def form_invalid(self, form):
    """
    Ensures response has 422 status on when the form was invalid.
    """
    response = old_form_invalid(self, form)
    response.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    return response


FormMixin.form_valid = form_valid
FormMixin.form_invalid = form_invalid
