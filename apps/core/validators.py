from typing import Iterable, Optional

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from magic import from_buffer


@deconstructible
class FileTypeValidator:
    """
    A model field validator that make sure the file type is valid.
    """

    message = "File type is incorrect!"
    code = "invalid_file_type"

    def __init__(self, allowed_types: Iterable[int], message: Optional[str] = None):
        self.allowed_types = allowed_types
        if message is not None:
            self.message = message

    def __call__(self, value):
        mime = from_buffer(value.read(), mime=True)
        if mime not in self.allowed_types:
            raise ValidationError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.allowed_types == other.allowed_types
            and self.message == other.message
            and self.code == other.code
        )
