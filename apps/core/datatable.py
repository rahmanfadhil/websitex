from typing import List, Optional, Type

from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Paginator
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import html_safe
from django.utils.text import capfirst


class InvalidActionException(Exception):
    pass


class InvalidColumnException(Exception):
    pass


@html_safe
class DataTable:
    model: Optional[Type[Model]] = None
    fields: List[str] = []
    actions: List[str] = []

    template_name = "core/datatable.html"
    per_page_choices = (10, 20, 50, 100, 200, 500)

    def __init__(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> None:
        self.request = request
        self.queryset = queryset

        # Get entries per page number
        per_page = self.request.GET.get("per_page")
        if per_page and per_page.isnumeric() and int(per_page) in self.per_page_choices:
            per_page = int(per_page)
        else:
            per_page = self.per_page_choices[0]

        paginator = Paginator(queryset, per_page)
        page = paginator.page(self.request.GET.get("page", 1))
        self.page_obj = page

    @property
    def columns(self):
        """Get the column names for the table."""
        for field in self.fields:
            try:
                yield self.model._meta.get_field(field).verbose_name
            except FieldDoesNotExist as e:
                if not hasattr(self.model, field):
                    raise e
                yield capfirst(field.replace("_", " ").strip())

    @property
    def rows(self):
        """Get the table row values."""
        for instance in self.page_obj.object_list:
            yield (instance.pk, self._get_object_values(instance))

    def _get_object_values(self, instance):
        """
        Returns an iterable of each column values for a model instance.

        First, it will check if the inherited DataTable class has a property or
        method with it's name is registered in the `fields` property. Then, it
        will check if the model has a property of that name. If neither found,
        it will raise an InvalidColumnException.
        """
        for field in self.fields:
            if hasattr(self, field):
                value = getattr(self, field)
                if callable(value):
                    value = value(instance)
                yield value
            elif hasattr(instance, field):
                yield getattr(instance, field)
            else:
                raise InvalidColumnException

    @property
    def action_choices(self):
        """Get the available action."""
        for action in self.actions:
            yield (action, capfirst(action.replace("_", " ").strip()))

    def perform_action(self):
        """
        Handle when the user tries to perform an action to the selected items in
        the table.
        """

        # Get the selected items from the table.
        pk_list = self.request.POST.getlist("pk", [])
        self.queryset = self.queryset.filter(pk__in=pk_list)

        # Get the action method name.
        action = self.request.POST.get("datatable_action")

        # If the action is valid.
        if action and hasattr(self, action) and action in self.actions:
            # Call the action function.
            if isinstance(action, str):
                response = getattr(self, action)()
            elif callable(action):
                response = action(self.request, self.queryset)
            else:
                raise InvalidActionException

            # Returns a custom response from the action if defined.
            if response is not None:
                return response

        # If the action doesn't return anything, redirect to the current page.
        return redirect(self.request.path_info)

    def __str__(self):
        return render_to_string(self.template_name, {"datatable": self}, self.request)
