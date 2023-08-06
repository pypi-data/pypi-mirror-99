# -*- coding: utf-8 -*-
"""Contains element middleware."""

from enum import Enum
from typing import Union

from ..core.font import Font as FontCore
from ..core.image import Image as ImageCore
from .exceptions.element import (InvalidElementNameError,
                                 InvalidElementTypeError,
                                 InvalidElementValueError,
                                 InvalidFontColorError, InvalidFontError,
                                 InvalidFontSizeError, InvalidTextOffsetError,
                                 InvalidWrapLengthError)


class ElementType(Enum):
    """A enum to represent types of elements."""

    text = "text"
    checkbox = "checkbox"
    image = "image"
    radio = "radio"


class Element:
    """A class to represent an element of a PDF form."""

    def __init__(
        self,
        element_name: str,
        element_type: "ElementType",
        element_value: Union[str, bool, bytes, int] = None,
    ) -> None:
        """Constructs all attributes for the Element object."""

        self._name = element_name
        self._type = element_type
        self.value = element_value

        if element_type == ElementType.text:
            self.font = None
            self.font_size = None
            self.font_color = None
            self.text_x_offset = None
            self.text_y_offset = None
            self.text_wrap_length = None

    @property
    def name(self) -> str:
        """Name of the element."""

        return self._name

    @property
    def type(self) -> "ElementType":
        """Type of the element."""

        return self._type

    def validate_constants(self) -> None:
        """Validates unchangeable attributes of the element."""

        if not isinstance(self._name, str):
            raise InvalidElementNameError

        if not isinstance(self._type, ElementType):
            raise InvalidElementTypeError

    def validate_value(self) -> None:
        """Validates the value of the element."""

        if self._type == ElementType.text:
            if self.value is not None and not isinstance(self.value, str):
                raise InvalidElementValueError

        if self._type == ElementType.checkbox:
            if self.value is not None and not isinstance(self.value, bool):
                raise InvalidElementValueError

        if self._type == ElementType.image:
            if self.value is not None:
                if not isinstance(self.value, bytes):
                    raise InvalidElementValueError
                if not ImageCore().is_image(self.value):
                    raise InvalidElementValueError

        if self._type == ElementType.radio:
            if self.value is not None and not isinstance(self.value, int):
                raise InvalidElementValueError

    def validate_text_attributes(self) -> None:
        """Validates text element's attributes."""

        if self._type == ElementType.text:
            if (self.font is not None and not isinstance(self.font, str)) or (
                not FontCore().is_registered(self.font)
            ):
                raise InvalidFontError

            if self.font_size is not None and not isinstance(
                self.font_size, (float, int)
            ):
                raise InvalidFontSizeError

            if self.font_color is not None and not (
                isinstance(self.font_color, tuple) and len(self.font_color) == 3
            ):
                raise InvalidFontColorError

            if isinstance(self.font_color, tuple):
                for each in self.font_color:
                    if not isinstance(each, (float, int)):
                        raise InvalidFontColorError

            if self.text_x_offset is not None and not (
                isinstance(self.text_x_offset, (float, int))
            ):
                raise InvalidTextOffsetError

            if self.text_y_offset is not None and not (
                isinstance(self.text_y_offset, (float, int))
            ):
                raise InvalidTextOffsetError

            if self.text_wrap_length is not None and not isinstance(
                self.text_wrap_length, int
            ):
                raise InvalidWrapLengthError
