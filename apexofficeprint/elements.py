"""
Elements are used to replace the various tags in a template with actual data.
"""

import json
from ._utils import file_utils
from copy import deepcopy
from typing import Union, List, Iterable, Mapping, Set, FrozenSet
from abc import abstractmethod, ABC
from collections.abc import MutableSet
from logging import warn


class CellStyle:
    def __init__(self, background_color: str = None, width: str = None):
        self.background_color: str = background_color
        self.width: Union[str, int] = width

    def get_dict(self, property_name: str):
        result = {}
        for suffix, value in self._dict_suffixes.items():
            result[property_name + suffix] = value
        return result

    @property
    def _dict_suffixes(self):
        result = {}

        if self.background_color:
            result["_background_color"] = self.background_color
        if self.width:
            result["_width"] = self.width

        return result


class TextStyle:
    def __init__(self,
                 italic: bool = None,
                 bold: bool = None,
                 color: str = None,
                 font: str = None):
        self.italic: bool = italic
        self.bold: bool = bold
        self.color: str = color
        self.font: str = font

    @property
    def as_dict(self):
        result = {}

        if self.italic is not None:
            result["italic"] = self.italic
        if self.bold is not None:
            result["bold"] = self.bold
        if self.color:
            result["color"] = self.color
        if self.font:
            result["font"] = self.font

        return result


class Element(ABC):
    """ The abstract base class for elements."""

    def __init__(self, name: str):
        self.name = name
        """Name for this element

        Returns:
            str: element name
        """

    def __str__(self):
        return self.json

    def __repr__(self):
        return self.json

    @property
    def json(self) -> str:
        """json representation of this `Element`.

        Isomorphic with the dict representation (`Element.as_dict`).

        Returns:
            str: json representation
        """
        return json.dumps(self.as_dict)

    @property
    @abstractmethod
    def as_dict(self) -> dict:
        """Dictionary representation of this `Element`.

        Isomorphic with the json representation (`Element.json`).

        Returns:
            dict: dictionary representation
        """
        pass

    @property
    @abstractmethod
    def available_tags(self) -> FrozenSet[str]:
        """A `frozenset` containing all available template tags this `Element` reacts to.

        Returns:
            FrozenSet[str]: set of tags associated with this `Element`
        """
        pass


class Property(Element):
    """The most basic `Element`. It simply consists of a name and a value.

    In a template, `{name}` is replaced by `value`.
    """

    def __init__(self, name: str, value: str, cell_style: CellStyle = None):
        super().__init__(name)
        self.value: Union[int, str] = value
        """Value of this property."""
        self.cell_style: CellStyle = cell_style
        """Cell style for this property.

        This is optional and will only work in an Excel file or inside e.g. a table in a docx file.
        Note: the tag required for applying cell markup is `{name$}` instead of `{name}`.
        """

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        if self.cell_style:
            for suffix, value in self.cell_style._dict_suffixes.items():
                result[self.name + suffix] = value

        return result


class ForEach(Element):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name)
        self._content = list(content)
        self._tags = {
            "{#" + name + "}",
            "{/" + name + "}"
        }

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: Iterable[Element]):
        self._content = value

    @property
    def available_tags(self) -> FrozenSet[str]:
        result = self._tags

        for element in self.content:
            result |= element.available_tags

        return frozenset(result)

    @property
    def as_dict(self):
        return {
            self.name: [element.as_dict for element in self.content]
        }


class Labels(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{-" + name + "}"
        }


class ForEachSlide(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{!" + name + "}"
        }


class ForEachInline(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{:" + name + "}",
            "{/" + name + "}"
        }


class ForEachTableRow(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{=" + name + "}",
            "{/" + name + "}"
        }


# These are the same, but they may not be forever
# and combining them into one class breaks consistency
ForEachSheet = ForEachSlide  # TODO: sheet name
ForEachHorizontal = ForEachInline


class Html(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{_" + self.name + "}"})


class Image(Element, ABC):
    """The abstract base class for image elements."""

    def __init__(self,
                 name: str,
                 max_width: int,
                 max_height: int,
                 alt_text: str,
                 wrap_text: str,
                 rotation: int):
        super().__init__(name)
        self.max_width: int = max_width
        """ """
        self.max_height: int = max_height
        """ """
        self.alt_text: str = alt_text
        self.wrap_text: str = wrap_text
        self.rotation: int = rotation

    @property
    def alt_text(self) -> str:
        return self._alt_text

    @alt_text.setter
    def alt_text(self, value: str):
        self._alt_text = None if value == "" else value

    @property
    def wrap_text(self) -> str:
        return self._wrap_text if self._wrap_text else "inline"

    @wrap_text.setter
    def wrap_text(self, value: str):
        self._wrap_text = None if value == "inline" else value

    @property
    def rotation(self) -> int:
        return self._rotation if self._rotation else 0

    @rotation.setter
    def rotation(self, value: int):
        self._rotation = None if value == 0 else value

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{%" + self.name + "}"})

    @property
    def _dict_suffixes(self):
        result = {}

        if self.max_width:
            result["_max_width"] = self.max_width
        if self.max_height:
            result["_max_height"] = self.max_height
        if self._alt_text:
            result["_alt_text"] = self._alt_text
        if self._wrap_text:
            result["_wrap_text"] = self._wrap_text
        if self._rotation:
            result["_rotation"] = self._rotation

        return result

    @staticmethod
    def from_file(name: str, path: str):
        return ImageBase64(name, file_utils.read_file_as_base64(path))

    @staticmethod
    def from_raw(name: str, data):
        return ImageBase64(name, file_utils.raw_to_base64(data))

    @staticmethod
    def from_base64(name: str, base64str: str):
        return ImageBase64(name, base64str)

    @staticmethod
    def from_url(name: str, url: str):
        return ImageUrl(name, url)


class ImageUrl(Image):
    def __init__(self,
                 name: str,
                 url: str,
                 max_width: int = None,
                 max_height: int = None,
                 alt_text: str = "",
                 wrap_text: str = "inline",
                 rotation: int = None):
        super().__init__(name, max_width, max_height, alt_text, wrap_text, rotation)
        self.url: str = url

    @property
    def as_dict(self) -> dict:
        result = {
            self.name + "_url": self.url
        }

        for suffix, value in self._dict_suffixes.items():
            result[self.name + suffix] = value

        return result


class ImageBase64(Image):
    def __init__(self,
                 name: str,
                 base64str: str,
                 max_width: int = None,
                 max_height: int = None,
                 alt_text: str = None,
                 wrap_text: str = "inline",
                 rotation: int = None):
        super().__init__(name, max_width, max_height, alt_text, wrap_text, rotation)
        self.base64: str = base64str

    @property
    def as_dict(self) -> dict:
        result = {
            self.name: self.base64
        }

        for suffix, value in self._dict_suffixes.items():
            result[self.name + suffix] = value

        return result


class Code(Element):
    """# TODO: refer to this link for type argument
    http://www.apexofficeprint.com/docs/#615-barcode-qrcode-tags
    """

    def __init__(self,
                 name: str,
                 data: str,
                 height: int = None,
                 width: int = None,
                 link_url: str = None,
                 rotation: int = None,
                 background_color: str = None,
                 padding_width: int = None,
                 padding_height: int = None,
                 qr_error_correction_level: str = None):
        super().__init__(name)
        self.data: str = data
        self.height: int = height
        self.width: int = width
        self.link_url: str = link_url
        self.rotation: int = rotation
        self.background_color: str = background_color
        self.padding_width: int = padding_width
        self.padding_height: int = padding_height
        self.qr_error_correction_level: str = qr_error_correction_level

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{|" + self.name + "}"})

    @property
    def _dict_suffixes(self):
        result = {}

        if self.height:
            result["_height"] = self.height
        if self.width:
            result["_width"] = self.width
        if self.link_url:
            result["_url"] = self.link_url
        if self.rotation:
            result["_rotation"] = self.rotation
        if self.background_color:
            result["_background_color"] = self.background_color
        if self.padding_width:
            result["_padding_width"] = self.padding_width
        if self.padding_height:
            result["_padding_height"] = self.padding_height
        if self.qr_error_correction_level:
            result["_errorcorrectlevel"] = self.qr_error_correction_level

        return result

    @property
    def as_dict(self) -> dict:
        result = {
            self.name: self.data
        }

        for suffix, value in self._dict_suffixes.items():
            result[self.name + suffix] = value

        return result


class DateOptions:
    def __init__(self,
                 format: str = None,
                 code: str = None,
                 unit: str = None,
                 step: Union[int, str] = None):
        self.format: str = format,
        self.code: str = code,
        self.unit: str = unit,
        self.step: Union[int, str] = step

    @property
    def as_dict(self):
        result = {}

        if self.format:
            result["format"] = self.format
        if self.code:
            result["code"] = self.code
        if self.unit:
            result["unit"] = self.unit
        if self.step:
            result["step"] = self.step

        return result


class ChartAxis:
    def __init__(self,
                 orientation: str = None,
                 min: Union[int, float] = None,
                 max: Union[int, float] = None,
                 date: DateOptions = None,
                 title: str = None,
                 values: bool = None,
                 values_style: TextStyle = None,
                 title_style: TextStyle = None,
                 title_rotation: int = None,
                 major_grid_lines: bool = None,
                 major_unit: Union[int, float] = None,
                 minor_grid_lines: bool = None,
                 minor_unit: Union[int, float] = None):
        self.orientation: str = orientation
        self.min: Union[int, float] = min
        self.max: Union[int, float] = max
        self.date: DateOptions = date
        self.title: str = title
        self.values: bool = values
        self.values_style: TextStyle = values_style
        self.title_style: TextStyle = title_style
        self.title_rotation: int = title_rotation
        self.major_grid_lines: bool = major_grid_lines
        self.major_unit: Union[int, float] = major_unit
        self.minor_grid_lines: bool = minor_grid_lines
        self.minor_unit: Union[int, float] = minor_unit

    @property
    def as_dict(self):
        result = {}

        if self.orientation:
            result["orientation"] = self.orientation
        if self.min:
            result["min"] = self.min
        if self.max:
            result["max"] = self.max
        if self.date:
            result["type"] = "date"
            result["date"] = self.date.as_dict
        if self.title:
            result["title"] = self.title
        if self.values is not None:
            result["showValues"] = self.values
        if self.values_style:
            result["valuesStyle"] = self.values_style.as_dict
        if self.title_style:
            result["titleStyle"] = self.title_style.as_dict
        if self.title_rotation:
            result["titleRotation"] = self.title_rotation
        if self.major_grid_lines is not None:
            result["majorGridlines"] = self.major_grid_lines
        if self.major_unit:
            result["majorUnit"] = self.major_unit
        if self.minor_grid_lines is not None:
            result["minorGridlines"] = self.minor_grid_lines
        if self.minor_unit:
            result["minorUnit"] = self.minor_unit

        return result


class Chart(Element):
    # TODO: document
    def __init__(self,
                 name: str,
                 x_axis: ChartAxis,
                 y_axis: ChartAxis,
                 y2_axis: ChartAxis = None,
                 width: int = None,
                 height: int = None,
                 border: bool = None,
                 rounded_corners: bool = None,
                 background_color: str = None,
                 background_opacity: int = None,
                 title: str = None,
                 title_style: TextStyle = None
                 ):
        super().__init__(name)
        self._legend_options = None

        self.x_axis: ChartAxis = x_axis
        self.y_axis: ChartAxis = y_axis
        self.y2_axis: ChartAxis = y2_axis
        if y_axis.date or y2_axis.date:
            warn('"date" options for the y or y2 axes are ignored by the AOP server.')

        self.width: int = width
        self.height: int = height
        self.border: bool = border
        self.rounded_corners: bool = rounded_corners
        self.background_color: str = background_color
        self.background_opacity: int = background_opacity
        self.title: str = title
        self.title_style: TextStyle = title_style

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$" + self.name + "}"})

    def set_legend(self, position: str = 'r', style: TextStyle = None):
        self._legend_options = {
            "showLegend": True
        }
        if position:
            self._legend_options["position"] = position
        if style:
            self._legend_options["style"] = style.as_dict

    def remove_legend(self):
        self._legend_options = None

    def set_data_labels(self,
                        separator: bool = None,
                        series_name: bool = None,
                        category_name: bool = None,
                        legend_key: bool = None,
                        value: bool = None,
                        percentage: bool = None,
                        position: str = None):
        self._data_labels_options = {
            "showDataLabels": True
        }
        if separator:
            self._data_labels_options["separator"] = True
        if series_name:
            self._data_labels_options["showSeriesName"] = True
        if category_name:
            self._data_labels_options["showCategoryName"] = True
        if legend_key:
            self._data_labels_options["showLegendKey"] = True
        if value:
            self._data_labels_options["showValue"] = True
        if percentage:
            self._data_labels_options["showPercentage"] = True
        if position:
            self._data_labels_options["position"] = position

    def remove_data_labels(self):
        self._data_labels_options = None

    @property
    def as_dict(self):
        result = {
            "axis": {
                "x": self.x_axis.as_dict,
                "y": self.y_axis.as_dict
            }
        }

        if self.y2_axis:
            result["axis"]["y2"] = self.y2_axis.as_dict
        if self.width:
            result["width"] = self.width
        if self.height:
            result["height"] = self.height
        if self.border is not None:
            result["border"] = self.border
        if self.rounded_corners is not None:
            result["roundedCorners"] = self.rounded_corners
        if self.background_color:
            result["backgroundColor"] = self.background_color
        if self.background_opacity:
            result["backgroundOpacity"] = self.background_opacity
        if self.title:
            result["title"] = self.title
        if self.title_style:
            result["title_style"] = self.title_style.as_dict
        if self._legend_options:
            result["legend"] = self._legend_options
        if self._data_labels_options:
            result["dataLabels"] = self._data_labels_options

        return result


class Object(list, Element):
    """# TODO
    """

    def __init__(self, name: str = "", elements: Iterable[Element] = []):
        # name not used for outer element
        list.__init__(self, elements)
        Element.__init__(self, name)

    def __str__(self):
        return self.json

    def __repr__(self):
        return self.json

    def copy(self):
        return self.__class__(self)

    def deepcopy(self):
        return deepcopy(self)

    @property
    def json(self):
        return json.dumps(self.as_dict)

    def add(self, element: Element):
        self.append(element)

    def add_all(self, obj: 'Object'):
        for element in obj:
            self.add(element)

    def remove_element_by_name(self, element_name: str):
        self.remove(
            next(element for element in self if element.name == element_name)
        )

    @property
    def as_dict(self) -> dict:
        """Merge the `Object`'s contents as one dict.

        Returns:
            dict: merged element
        """
        result = {}
        for element in self:
            result.update(element.as_dict)
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        result = set()
        for element in self:
            result |= element.available_tags
        return frozenset(result)

    @classmethod
    def from_mapping(cls, mapping: Mapping, name: str = "") -> 'Object':
        result_set = set()
        for key, value in mapping.items():
            result_set.add(Property(key, value))
        return cls(name, result_set)

    @classmethod
    def from_json(cls, json_str: str, name: str = "") -> 'Object':
        return cls.from_mapping(json.loads(json_str), name)
