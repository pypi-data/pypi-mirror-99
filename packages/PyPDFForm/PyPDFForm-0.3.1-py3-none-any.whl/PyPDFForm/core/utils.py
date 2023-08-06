# -*- coding: utf-8 -*-
"""Contains utility helpers."""

from copy import deepcopy
from io import BytesIO
from typing import Dict, Union

import pdfrw


class Utils:
    """Contains utility methods for core modules."""

    @staticmethod
    def generate_stream(pdf: "pdfrw.PdfReader") -> bytes:
        """Generates new stream for manipulated PDF form."""

        result_stream = BytesIO()

        pdfrw.PdfWriter().write(result_stream, pdf)
        result_stream.seek(0)

        result = result_stream.read()
        result_stream.close()

        return result

    @staticmethod
    def bool_to_checkboxes(
        data: Dict[str, Union[str, bool, bytes, int]]
    ) -> Dict[str, Union[str, "pdfrw.PdfName"]]:
        """Converts all boolean values in input data dictionary into PDF checkbox objects."""

        result = deepcopy(data)

        for key, value in result.items():
            if isinstance(value, bool):
                result[key] = pdfrw.PdfName.Yes if value else pdfrw.PdfName.Off

        return result

    @staticmethod
    def bool_to_checkbox(data: bool) -> "pdfrw.PdfName":
        """Converts a boolean value into a PDF checkbox object."""

        return pdfrw.PdfName.Yes if data else pdfrw.PdfName.Off

    @staticmethod
    def merge_two_pdfs(pdf: bytes, other: bytes) -> bytes:
        """Merges two PDFs into one PDF."""

        writer = pdfrw.PdfWriter()

        writer.addpages(pdfrw.PdfReader(fdata=pdf).pages)
        writer.addpages(pdfrw.PdfReader(fdata=other).pages)

        result_stream = BytesIO()
        writer.write(result_stream)
        result_stream.seek(0)

        result = result_stream.read()
        result_stream.close()

        return result
