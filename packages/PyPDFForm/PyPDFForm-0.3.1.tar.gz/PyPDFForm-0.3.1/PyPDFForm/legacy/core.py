# -*- coding: utf-8 -*-

import uuid
from io import BytesIO
from typing import List, Tuple, Union

import pdfrw
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as canv

from .element import Element
from .exceptions import (InvalidCoordinateError, InvalidEditableParameterError,
                         InvalidFontColorError, InvalidFontSizeError,
                         InvalidFormDataError, InvalidImageDimensionError,
                         InvalidImageError, InvalidImageRotationAngleError,
                         InvalidModeError, InvalidPageNumberError,
                         InvalidTemplateError, InvalidTextError,
                         InvalidTextOffsetError, InvalidWrapLengthError)


class _PyPDFForm(object):
    """Core components of PyPDFForm."""

    def __init__(self) -> None:
        """Constructs all attributes for the core object."""

        self._ANNOT_KEY = "/Annots"
        self._ANNOT_FIELD_KEY = "/T"
        self._ANNOT_RECT_KEY = "/Rect"
        self._SUBTYPE_KEY = "/Subtype"
        self._WIDGET_SUBTYPE_KEY = "/Widget"
        self._ANNOT_TYPE_KEY = "/FT"

        self._CANVAS_FONT = "Helvetica"
        self._GLOBAL_FONT_SIZE = 12
        self._GLOBAL_FONT_COLOR = (0, 0, 0)
        self._MAX_TXT_LENGTH = 100

        self._uuid = uuid.uuid4().hex

        self._data_dict = {}
        self.elements = {}

        self.stream = b""

    def __add__(self, other: "_PyPDFForm") -> "_PyPDFForm":
        """Overloaded addition operator to perform merging PDFs."""

        if not self.stream:
            return other

        self._validate_template(self.stream)
        self._validate_template(other.stream)

        writer = pdfrw.PdfWriter()

        writer.addpages(pdfrw.PdfReader(fdata=self.stream).pages)
        writer.addpages(pdfrw.PdfReader(fdata=other.stream).pages)

        result_stream = BytesIO()
        writer.write(result_stream)
        result_stream.seek(0)

        new_obj = self.__class__()
        new_obj.stream = result_stream.read()

        result_stream.close()

        return new_obj

    @staticmethod
    def _validate_template(template_stream: bytes) -> None:
        """Validate if a template stream is indeed a PDF stream."""

        if b"%PDF" not in template_stream:
            raise InvalidTemplateError

    @staticmethod
    def _validate_fill_inputs(
        data: dict,
        simple_mode: bool,
        font_size: Union[float, int],
        font_color: Tuple[Union[float, int], Union[float, int], Union[float, int]],
        text_x_offset: Union[float, int],
        text_y_offset: Union[float, int],
        text_wrap_length: int,
        editable: bool,
    ) -> None:
        """Validate input parameters for the fill method."""

        if not isinstance(data, dict):
            raise InvalidFormDataError

        if not isinstance(simple_mode, bool):
            raise InvalidModeError

        if not (isinstance(font_size, float) or isinstance(font_size, int)):
            raise InvalidFontSizeError

        if font_color and not (isinstance(font_color, tuple) and len(font_color) == 3):
            raise InvalidFontColorError

        if isinstance(font_color, tuple):
            for each in font_color:
                if not (isinstance(each, float) or isinstance(each, int)):
                    raise InvalidFontColorError

        if not isinstance(text_wrap_length, int):
            raise InvalidWrapLengthError

        if not (isinstance(text_x_offset, float) or isinstance(text_x_offset, int)):
            raise InvalidTextOffsetError

        if not (isinstance(text_y_offset, float) or isinstance(text_y_offset, int)):
            raise InvalidTextOffsetError

        if not (isinstance(editable, bool)):
            raise InvalidEditableParameterError

    @staticmethod
    def _validate_draw_text_inputs(
        text: str,
        page_number: int,
        x: Union[float, int],
        y: Union[float, int],
    ) -> None:
        """Validate input parameters for the draw text method."""

        if not isinstance(text, str):
            raise InvalidTextError

        if not isinstance(page_number, int):
            raise InvalidPageNumberError

        if not (isinstance(x, float) or isinstance(x, int)):
            raise InvalidCoordinateError

        if not (isinstance(y, float) or isinstance(y, int)):
            raise InvalidCoordinateError

    @staticmethod
    def _validate_draw_image_inputs(
        page_number: int,
        x: Union[float, int],
        y: Union[float, int],
        width: Union[float, int],
        height: Union[float, int],
        rotation: Union[float, int],
    ) -> None:
        """Validate input parameters for the draw image method."""

        if not isinstance(page_number, int):
            raise InvalidPageNumberError

        if not (isinstance(x, float) or isinstance(x, int)):
            raise InvalidCoordinateError

        if not (isinstance(y, float) or isinstance(y, int)):
            raise InvalidCoordinateError

        if not (isinstance(width, float) or isinstance(width, int)):
            raise InvalidImageDimensionError

        if not (isinstance(height, float) or isinstance(height, int)):
            raise InvalidImageDimensionError

        if not (isinstance(rotation, float) or isinstance(rotation, int)):
            raise InvalidImageRotationAngleError

    def _iterate_elements(self, pdf: "pdfrw.PdfReader") -> List["pdfrw.PdfDict"]:
        """Iterates through a PDF and returns all elements found."""

        result = []

        for i in range(len(pdf.pages)):
            elements = pdf.pages[i][self._ANNOT_KEY]
            if elements:
                for element in elements:
                    if (
                        element[self._SUBTYPE_KEY] == self._WIDGET_SUBTYPE_KEY
                        and element[self._ANNOT_FIELD_KEY]
                    ):
                        result.append(element)

        return result

    def _bool_to_checkboxes(self) -> None:
        """Converts all boolean values in input data dictionary into PDF checkbox objects."""

        for k, v in self._data_dict.items():
            if isinstance(v, bool):
                self._data_dict[k] = pdfrw.PdfName.Yes if v else pdfrw.PdfName.Off

    def _checkboxes_to_bool(self) -> None:
        """Converts all PDF checkbox objects back to boolean values."""

        checkbox_mapping = {pdfrw.PdfName.Yes: True, pdfrw.PdfName.Off: False}

        for k, v in self._data_dict.items():
            if v in checkbox_mapping.keys():
                self._data_dict[k] = checkbox_mapping[v]

    def _assign_uuid(self, output_stream: bytes, editable: bool) -> bytes:
        """Append UUIDs to all elements of the PDF form."""

        _uuid = self._uuid

        generated_pdf = pdfrw.PdfReader(fdata=output_stream)

        for element in self._iterate_elements(generated_pdf):
            if editable:
                update_obj = pdfrw.PdfDict(
                    T="{}_{}".format(
                        element[self._ANNOT_FIELD_KEY][1:-1],
                        _uuid,
                    ),
                )
            else:
                update_obj = pdfrw.PdfDict(
                    T="{}_{}".format(
                        element[self._ANNOT_FIELD_KEY][1:-1],
                        _uuid,
                    ),
                    Ff=pdfrw.PdfObject(1),
                )

            element.update(update_obj)

        result_stream = BytesIO()
        pdfrw.PdfWriter().write(result_stream, generated_pdf)
        result_stream.seek(0)

        result = result_stream.read()
        result_stream.close()

        return result

    def _fill_pdf(self, template_stream: bytes) -> bytes:
        """Fill a PDF form in simple mode."""

        template_pdf = pdfrw.PdfReader(fdata=template_stream)

        for element in self._iterate_elements(template_pdf):
            key = element[self._ANNOT_FIELD_KEY][1:-1]
            if key in self._data_dict.keys():
                element.update(
                    pdfrw.PdfDict(
                        V="{}".format(self._data_dict[key]),
                        AS=self._data_dict[key],
                    )
                )

        result_stream = BytesIO()
        pdfrw.PdfWriter().write(result_stream, template_pdf)
        result_stream.seek(0)

        result = result_stream.read()

        result_stream.close()

        return result

    def _fill_pdf_canvas(
        self,
        template_stream: bytes,
        text_x_offset: Union[float, int],
        text_y_offset: Union[float, int],
    ) -> bytes:
        """Fill a PDF form by drawing on a reportlab canvas."""

        template_pdf = pdfrw.PdfReader(fdata=template_stream)
        layers = []

        for i in range(len(template_pdf.pages)):
            layer = BytesIO()
            layers.append(layer)

            c = canv.Canvas(
                layer,
                pagesize=(
                    float(template_pdf.pages[i].MediaBox[2]),
                    float(template_pdf.pages[i].MediaBox[3]),
                ),
            )

            elements = template_pdf.pages[i][self._ANNOT_KEY]
            if elements:
                for j in reversed(range(len(elements))):
                    element = elements[j]
                    c.setFont(self._CANVAS_FONT, self._GLOBAL_FONT_SIZE)
                    if self._GLOBAL_FONT_COLOR != (0, 0, 0):
                        c.setFillColorRGB(
                            self._GLOBAL_FONT_COLOR[0],
                            self._GLOBAL_FONT_COLOR[1],
                            self._GLOBAL_FONT_COLOR[2],
                        )

                    if (
                        element[self._SUBTYPE_KEY] == self._WIDGET_SUBTYPE_KEY
                        and element[self._ANNOT_FIELD_KEY]
                    ):
                        key = element[self._ANNOT_FIELD_KEY][1:-1]
                        if key in self._data_dict.keys():
                            if self._data_dict[key] in [
                                pdfrw.PdfName.Yes,
                                pdfrw.PdfName.Off,
                            ]:
                                element.update(
                                    pdfrw.PdfDict(
                                        AS=self._data_dict[key], Ff=pdfrw.PdfObject(1)
                                    )
                                )
                            else:
                                max_text_length = self._MAX_TXT_LENGTH
                                x_offset = text_x_offset
                                y_offset = text_y_offset

                                _element = self.elements[key]

                                if _element.type == "text":
                                    if _element.font_size:
                                        c.setFont(self._CANVAS_FONT, _element.font_size)
                                    if _element.font_color:
                                        c.setFillColorRGB(
                                            _element.font_color[0],
                                            _element.font_color[1],
                                            _element.font_color[2],
                                        )
                                    if _element.text_x_offset:
                                        x_offset = _element.text_x_offset
                                    if _element.text_y_offset:
                                        y_offset = _element.text_y_offset
                                    if _element.text_wrap_length:
                                        max_text_length = _element.text_wrap_length

                                coordinates = element[self._ANNOT_RECT_KEY]
                                elements.pop(j)
                                if len(self._data_dict[key]) < max_text_length:
                                    c.drawString(
                                        float(coordinates[0]) + x_offset,
                                        (float(coordinates[1]) + float(coordinates[3]))
                                        / 2
                                        - 2
                                        + y_offset,
                                        self._data_dict[key],
                                    )
                                else:
                                    txt_obj = c.beginText(0, 0)

                                    start = 0
                                    end = max_text_length

                                    while end < len(self._data_dict[key]):
                                        txt_obj.textLine(
                                            (self._data_dict[key][start:end])
                                        )
                                        start += max_text_length
                                        end += max_text_length
                                    txt_obj.textLine(self._data_dict[key][start:])
                                    c.saveState()
                                    c.translate(
                                        float(coordinates[0]) + x_offset,
                                        (float(coordinates[1]) + float(coordinates[3]))
                                        / 2
                                        - 2
                                        + y_offset,
                                    )
                                    c.drawText(txt_obj)
                                    c.restoreState()
                        else:
                            elements.pop(j)

            c.save()
            layer.seek(0)

        for i in range(len(template_pdf.pages)):
            layer_pdf = pdfrw.PdfReader(layers[i])
            input_page = template_pdf.pages[i]
            merger = pdfrw.PageMerge(input_page)

            if len(layer_pdf.pages) > 0:
                merger.add(layer_pdf.pages[0]).render()

            layers[i].close()

        result_stream = BytesIO()
        pdfrw.PdfWriter().write(result_stream, template_pdf)
        result_stream.seek(0)

        result = result_stream.read()
        result_stream.close()

        return result

    def draw_image(
        self,
        image_stream: bytes,
        page_number: int,
        x: Union[float, int],
        y: Union[float, int],
        width: Union[float, int],
        height: Union[float, int],
        rotation: Union[float, int],
    ) -> "_PyPDFForm":
        """Draw an image on a PDF form."""

        self._validate_template(self.stream)
        self._validate_draw_image_inputs(page_number, x, y, width, height, rotation)

        input_file = pdfrw.PdfReader(fdata=self.stream)

        buff = BytesIO()
        buff.write(image_stream)
        buff.seek(0)

        try:
            image = Image.open(buff)
        except Exception:
            raise InvalidImageError

        image_buff = BytesIO()
        image.rotate(rotation, expand=True).save(image_buff, format=image.format)
        image_buff.seek(0)

        canv_buff = BytesIO()

        c = canv.Canvas(
            canv_buff,
            pagesize=(
                float(input_file.pages[page_number - 1].MediaBox[2]),
                float(input_file.pages[page_number - 1].MediaBox[3]),
            ),
        )

        c.drawImage(ImageReader(image_buff), x, y, width=width, height=height)
        c.save()
        canv_buff.seek(0)

        output_file = pdfrw.PdfFileWriter()

        for i in range(len(input_file.pages)):
            if i == page_number - 1:
                merger = pdfrw.PageMerge(input_file.pages[i])
                merger.add(pdfrw.PdfReader(fdata=canv_buff.read()).pages[0]).render()

        result_stream = BytesIO()
        output_file.write(result_stream, input_file)
        result_stream.seek(0)
        self.stream = result_stream.read()

        buff.close()
        image_buff.close()
        canv_buff.close()
        result_stream.close()

        return self

    def draw_text(
        self,
        text: str,
        page_number: int,
        x: Union[float, int],
        y: Union[float, int],
    ) -> "_PyPDFForm":
        """Draw a text on a PDF form."""

        self._validate_template(self.stream)
        self._validate_draw_text_inputs(text, page_number, x, y)

        input_file = pdfrw.PdfReader(fdata=self.stream)

        canv_buff = BytesIO()

        c = canv.Canvas(
            canv_buff,
            pagesize=(
                float(input_file.pages[page_number - 1].MediaBox[2]),
                float(input_file.pages[page_number - 1].MediaBox[3]),
            ),
        )

        c.drawString(x, y, text)
        c.save()
        canv_buff.seek(0)

        output_file = pdfrw.PdfFileWriter()

        for i in range(len(input_file.pages)):
            if i == page_number - 1:
                merger = pdfrw.PageMerge(input_file.pages[i])
                merger.add(pdfrw.PdfReader(fdata=canv_buff.read()).pages[0]).render()

        result_stream = BytesIO()
        output_file.write(result_stream, input_file)
        result_stream.seek(0)
        self.stream = result_stream.read()

        canv_buff.close()
        result_stream.close()

        return self

    def fill(
        self,
        template_stream: bytes,
        data: dict,
        simple_mode: bool,
        font_size: Union[float, int],
        font_color: Tuple[Union[float, int], Union[float, int], Union[float, int]],
        text_x_offset: Union[float, int],
        text_y_offset: Union[float, int],
        text_wrap_length: int,
        editable: bool,
    ) -> "_PyPDFForm":
        """General wrapper for filling a PDF form."""

        self._validate_template(template_stream)
        self._validate_fill_inputs(
            data,
            simple_mode,
            font_size,
            font_color,
            text_x_offset,
            text_y_offset,
            text_wrap_length,
            editable,
        )

        self._GLOBAL_FONT_SIZE = font_size
        self._GLOBAL_FONT_COLOR = font_color
        self._MAX_TXT_LENGTH = text_wrap_length

        self._data_dict = data
        self._bool_to_checkboxes()

        if simple_mode:
            output_stream = self._fill_pdf(template_stream)
            self.stream = self._assign_uuid(output_stream, editable)
        else:
            self.stream = self._fill_pdf_canvas(
                template_stream, text_x_offset, text_y_offset
            )

        self._checkboxes_to_bool()

        if not simple_mode:
            self._update_elements(text_x_offset, text_y_offset)

        return self

    def _update_elements(
        self, text_x_offset: Union[float, int], text_y_offset: Union[float, int]
    ) -> None:
        """Updates elements' values given data dict."""

        for k, v in self.elements.items():
            v.value = self._data_dict.get(k)

            if v.type == "text":
                if not v.font_size:
                    v.font_size = self._GLOBAL_FONT_SIZE
                if not v.font_color:
                    v.font_color = self._GLOBAL_FONT_COLOR
                if not v.text_x_offset:
                    v.text_x_offset = text_x_offset
                if not v.text_y_offset:
                    v.text_y_offset = text_y_offset
                if not v.text_wrap_length:
                    v.text_wrap_length = self._MAX_TXT_LENGTH

    def build_elements(self, pdf_stream: bytes) -> "_PyPDFForm":
        """Builds an element list."""

        if not pdf_stream:
            return self

        self._validate_template(pdf_stream)

        element_type_mapping = {
            "/Btn": "checkbox",
            "/Tx": "text",
        }

        _pdf = pdfrw.PdfReader(fdata=pdf_stream)

        for element in self._iterate_elements(_pdf):
            key = element[self._ANNOT_FIELD_KEY][1:-1]

            self.elements[key] = Element(
                element_name=key,
                element_type=element_type_mapping.get(
                    str(element[self._ANNOT_TYPE_KEY])
                ),
            )

        return self
