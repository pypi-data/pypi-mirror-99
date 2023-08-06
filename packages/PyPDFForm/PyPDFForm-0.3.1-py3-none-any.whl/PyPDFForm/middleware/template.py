# -*- coding: utf-8 -*-
"""Contains helpers for template middleware."""

from typing import Dict

from ..core.template import Template as TemplateCore
from .element import Element
from .exceptions.template import InvalidTemplateError


class Template:
    """Contains methods for interacting with template middlewares."""

    @staticmethod
    def validate_template(pdf_stream: bytes) -> None:
        """Validates if a template stream is byte type."""

        if not isinstance(pdf_stream, bytes):
            raise InvalidTemplateError

    @staticmethod
    def validate_stream(pdf_stream: bytes) -> None:
        """Validates if a template stream is indeed a PDF stream."""

        if b"%PDF" not in pdf_stream:
            raise InvalidTemplateError

    @staticmethod
    def build_elements(pdf_stream: bytes) -> Dict[str, "Element"]:
        """Builds an element dict given a PDF form stream."""

        results = {}

        for element in TemplateCore().iterate_elements(pdf_stream):
            key = TemplateCore().get_element_key(element)

            results[key] = Element(
                element_name=key,
                element_type=TemplateCore().get_element_type(element),
            )

        return results
