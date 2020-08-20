"""
Elements are used to replace the various tags in a template with actual data.
"""
# TODO: split up? e.g. charts separate, and config should be split up again too

import json
from ._utils import file_utils
from copy import deepcopy
from typing import Union, Sequence, Tuple, Iterable, Mapping, Set, FrozenSet
from abc import abstractmethod, ABC
from collections.abc import MutableSet
from logging import warning


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


class ChartTextStyle:
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

    def __init__(self, name: str, value: str):
        super().__init__(name)
        self.value: Union[int, str] = value
        """Value of this property."""

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "}"})

    @property
    def as_dict(self):
        return {
            self.name: self.value
        }


class CellStyleProperty(Property):
    def __init__(self, name: str, value: str, cell_style: CellStyle):
        super().__init__(name, value)
        self.cell_style: CellStyle = cell_style
        """Cell style as a `CellStyle`."""

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "$}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        for suffix, value in self.cell_style._dict_suffixes.items():
            result[self.name + suffix] = value

        return result


class Html(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{_" + self.name + "}"})


class RightToLeft(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{<" + self.name + "}"})


class FootNote(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{+" + self.name + "}"})


class HyperLink(Element):
    def __init__(self, name: str, url: str, text: str = None):
        super().__init__(name)
        self.url: str = url
        self.text: str = text

    @property
    def available_tags(self):
        return frozenset({"{*" + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.url
        }

        if self.text:
            result[self.name + "_text"] = self.text

        return result


class TableOfContents(Element):
    def __init__(self, name: str, title: str, depth: int = None, tab_leader: str = None):
        super().__init__(name)
        self.title: str = title
        self.depth: int = None
        self.tab_leader: str = None

    @property
    def available_tags(self):
        return frozenset({"{~" + self.name + "}"})

    @property
    def as_dict(self):
        result = dict()

        if self.title:
            result[self.name + "_title"] = self.title
        if self.depth:
            result[self.name + "_show_level"] = self.depth
        if self.tab_leader:
            result[self.name + "_tab_leader"] = self.tab_leader

        return result


class Raw(Property):
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self):
        return frozenset({"{@" + self.name + "}"})


class Span(Property):
    def __init__(self, name: str, value: str, columns: int, rows: int):
        super().__init__(name, value)
        self.columns = columns
        self.rows = rows

    @property
    def available_tags(self):
        return frozenset({"{" + self.name + "#}"})

    @property
    def as_dict(self):
        return {
            self.name: self.value,
            self.name + "_row_span": self.rows,
            self.name + "_col_span": self.columns
        }


class Formula(Property):
    def __init__(self, name: str, formula: str):
        super().__init__(name, formula)

    @property
    def available_tags(self):
        return frozenset({"{>" + self.name + "}"})


class StyledProperty(Property):
    def __init__(self,
                 name: str,
                 value: str,
                 font: str = None,
                 font_size: Union[str, int] = None,
                 font_color: str = None,
                 bold: bool = None,
                 italic: bool = None,
                 underline: bool = None,
                 strikethrough: bool = None,
                 highlight_color: bool = None):
        super().__init__(name, value)
        self.font: str = font,
        self.font_size: Union[str, int] = font_size,
        self.font_color: str = font_color,
        self.bold: bool = bold,
        self.italic: bool = italic,
        self.underline: bool = underline,
        self.strikethrough: bool = strikethrough,
        self.highlight_color: bool = highlight_color

    @property
    def available_tags(self):
        return frozenset({"{style " + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        if self.font:
            result[self.name + "_font_family"] = self.font
        if self.font_size:
            result[self.name + "_font_size"] = self.font_size
        if self.font_color:
            result[self.name + "_font_color"] = self.font_color
        if self.bold is not None:
            result[self.name + "_bold"] = self.bold
        if self.italic is not None:
            result[self.name + "_italic"] = self.italic
        if self.underline is not None:
            result[self.name + "_underline"] = self.underline
        if self.strikethrough is not None:
            result[self.name + "_strikethrough"] = self.strikethrough
        if self.font_color:
            result[self.name + "_font_color"] = self.font_color

        return result


class Watermark(Property):
    def __init__(self,
                 name: str,
                 text: str,
                 color: str = None,
                 font: str = None,
                 width: Union[int, str] = None,
                 height: Union[int, str] = None,
                 opacity: float = None,
                 rotation: int = None):
        super().__init__(name, text)
        self.color: str = color,
        self.font: str = font,
        self.width: Union[int, str] = width,
        self.height: Union[int, str] = height,
        self.opacity: float = opacity,
        self.rotation: int = rotation

    @property
    def available_tags(self):
        return frozenset({"{watermark " + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        if self.color:
            result[self.name + "_color"] = self.color
        if self.font:
            result[self.name + "_font"] = self.font
        if self.width:
            result[self.name + "_width"] = self.width
        if self.height:
            result[self.name + "_height"] = self.height
        if self.opacity:
            result[self.name + "_opacity"] = self.opacity
        if self.rotation:
            result[self.name + "_rotation"] = self.rotation

        return result


class D3Code(Property):
    def __init__(self, name: str, code: str):
        super().__init__(name, code)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$d3 " + self.name + "}"})


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

# TODO: aopchart


class ChartAxisOptions:
    def __init__(self,
                 orientation: str = None,
                 min: Union[int, float] = None,
                 max: Union[int, float] = None,
                 date: DateOptions = None,
                 title: str = None,
                 values: bool = None,
                 values_style: ChartTextStyle = None,
                 title_style: ChartTextStyle = None,
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
        self.values_style: ChartTextStyle = values_style
        self.title_style: ChartTextStyle = title_style
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


class ChartOptions():
    # TODO: document
    def __init__(self,
                 name: str,
                 x_axis: ChartAxisOptions,
                 y_axis: ChartAxisOptions,
                 y2_axis: ChartAxisOptions = None,
                 width: int = None,
                 height: int = None,
                 border: bool = None,
                 rounded_corners: bool = None,
                 background_color: str = None,
                 background_opacity: int = None,
                 title: str = None,
                 title_style: ChartTextStyle = None):
        self._legend_options: dict = None

        self.x_axis: ChartAxisOptions = x_axis
        self.y_axis: ChartAxisOptions = y_axis
        self.y2_axis: ChartAxisOptions = y2_axis
        if y_axis.date or y2_axis.date:
            warning('"date" options for the y or y2 axes are ignored by the AOP server.')

        self.width: int = width
        self.height: int = height
        self.border: bool = border
        self.rounded_corners: bool = rounded_corners
        self.background_color: str = background_color
        self.background_opacity: int = background_opacity
        self.title: str = title
        self.title_style: ChartTextStyle = title_style

    def set_legend(self, position: str = 'r', style: ChartTextStyle = None):
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


class Series:
    def __init__(self, name: str = None):
        self.name: str = name

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name

        return result


class XYSeries(Series):
    def __init__(self,
                 x: Sequence[Union[int, float, str]],
                 y: Sequence[Union[int, float]],
                 name: str = None):
        super().__init__(name)
        self.x: Sequence[Union[int, float, str]] = x
        self.y: Sequence[Union[int, float]] = y

    @property
    def data(self):
        return [{
            "x": x,
            "y": y
        } for x, y in zip(self.x, self.y)]


class PieSeries(XYSeries):
    def __init__(self,
                 x: Sequence[Union[int, float, str]],
                 y: Sequence[Union[int, float]],
                 color: str):
        super().__init__(x, y)
        self.color = color

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name
        if self.color:
            result["color"] = self.color

        return result


class AreaSeries(XYSeries):
    def __init__(self,
                 x: Sequence[Union[int, float, str]],
                 y: Sequence[Union[int, float]],
                 name: str = None,
                 color: str = None,
                 opacity: float = None):
        super().__init__(x, y, name)
        self.color = color
        self.opacity = opacity

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name
        if self.color:
            result["color"] = self.color
        if self.opacity:
            result["opacity"] = self.opacity

        return result


class LineSeries(XYSeries):
    def __init__(self,
                 x: Sequence[Union[int, float, str]],
                 y: Sequence[Union[int, float]],
                 name: str = None,
                 smooth: bool = None,
                 symbol: str = None,
                 symbol_size: Union[str, int] = None,
                 color: str = None,
                 line_width: str = None,
                 line_style: str = None):
        super().__init__(x, y, name)
        self.smooth: bool = smooth
        self.symbol: str = symbol
        self.symbol_size: Union[str, int] = symbol_size
        self.color: str = color
        self.line_width: str = line_width
        self.line_style: str = line_style

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name
        if self.smooth:
            result["smooth"] = self.smooth
        if self.symbol:
            result["symbol"] = self.symbol
        if self.symbol_size:
            result["symbolSize"] = self.symbol_size
        if self.color:
            result["color"] = self.color
        if self.line_width:
            result["lineWidth"] = self.line_width
        if self.line_style:
            result["lineStyle"] = self.line_style

        return result


class BubbleSeries(Series):
    def __init__(self,
                 x: Sequence[Union[int, float, str]],
                 y: Sequence[Union[int, float]],
                 sizes: Sequence[Union[int, float]],
                 name: str = None):
        super().__init__(name)
        self.x: Sequence[Union[int, float, str]] = x
        self.y: Sequence[Union[int, float]] = y
        self.sizes: Sequence[Union[int, float]] = sizes

    @property
    def data(self):
        return [{
            "x": x,
            "y": y,
            "size": size
        } for x, y, size in zip(self.x, self.y, self.sizes)]


class StockSeries(Series):
    def __init__(self,
                 x: Sequence[Union[int, float, str]],
                 high: Sequence[Union[int, float]],
                 low: Sequence[Union[int, float]],
                 close: Sequence[Union[int, float]],
                 open_: Sequence[Union[int, float]] = None,
                 volume: Sequence[Union[int, float]] = None,
                 name=None):
        super().__init__(name)
        self.x: Sequence[Union[int, float, str]] = x
        self.high: Sequence[Union[int, float]] = high
        self.low: Sequence[Union[int, float]] = low
        self.close: Sequence[Union[int, float]] = close
        # open argument gets a trailing _ because open() is a built-in function
        self.open: Sequence[Union[int, float]] = open_
        self.volume: Sequence[Union[int, float]] = volume

    @property
    def data(self):
        result = [{
            "x": x,
            "high": high,
            "low": low,
            "close": close
        } for x, high, low, close in zip(self.x, self.high, self.low, self.close)]

        for i in range(len(result)):
            if self.open:
                result[i]["open"] = self.open[i]
            if self.volume:
                result[i]["volume"] = self.volume[i]

        return result


# better to have a series for every possible chart for future-proofing, in case their options diverge later
BarSeries = BarStackedSeries = BarStackedPercentSeries = ColumnSeries = ColumnStackedSeries = ColumnStackedPercentSeries = RadarSeries = ScatterSeries = XYSeries


class Chart(Element, ABC):
    def __init__(self, name: str, options: Union[ChartOptions, dict] = None):
        Element.__init__(self, name)
        self.options: Union[ChartOptions, dict] = options

    @property
    @abstractmethod
    def as_dict(self):
        pass

    def _get_dict(self, updates: dict):
        result = {}
        if self.options:
            result["options"] = self.options if isinstance(self.options, dict) else self.options.as_dict
        result.update(updates)
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$" + self.name + "}"})


class LineChart(Chart):
    def __init__(self, name: str, *lines: Union[LineSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.lines: Tuple[Union[LineSeries, XYSeries]] = lines

    @property
    def as_dict(self):
        return self._get_dict({
            "lines": [line.as_dict for line in self.lines],
            "type": "line"
        })


class BarChart(Chart):
    def __init__(self, name: str, *bars: Union[BarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.bars: Tuple[Union[BarSeries, XYSeries]] = bars

    @property
    def as_dict(self):
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "bar"
        })


class BarStackedChart(Chart):
    def __init__(self, name: str, *bars: Union[BarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.bars: Tuple[Union[BarSeries, XYSeries]] = bars

    @property
    def as_dict(self):
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "barStacked"
        })


class BarStackedPercentChart(Chart):
    def __init__(self, name: str, *bars: Union[BarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.bars: Tuple[Union[BarSeries, XYSeries]] = bars

    @property
    def as_dict(self):
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "barStackedPercent"
        })


class ColumnChart(Chart):
    def __init__(self, name: str, *columns: Union[ColumnSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnSeries, XYSeries]] = columns

    @property
    def as_dict(self):
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "column"
        })


class ColumnStackedChart(Chart):
    def __init__(self, name: str, *columns: Union[ColumnSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnSeries, XYSeries]] = columns

    @property
    def as_dict(self):
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "columnStacked"
        })


class ColumnStackedPercentChart(Chart):
    def __init__(self, name: str, *columns: Union[ColumnSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnSeries, XYSeries]] = columns

    @property
    def as_dict(self):
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "columnStackedPercent"
        })


class PieChart(Chart):
    def __init__(self, name: str, *pies: Union[PieSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.pies: Tuple[Union[PieSeries, XYSeries]] = pies

    @property
    def as_dict(self):
        return self._get_dict({
            "pies": [pie.as_dict for pie in self.pies],
            "type": "pie"
        })


class Pie3DChart(Chart):
    def __init__(self, name: str, *pies: Union[PieSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.pies: Tuple[Union[PieSeries, XYSeries]] = pies

    @property
    def as_dict(self):
        return self._get_dict({
            "pies": [pie.as_dict for pie in self.pies],
            "type": "pie3d"
        })


class DoughnutChart(Chart):
    def __init__(self, name: str, *doughnuts: Union[PieSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name)
        self.doughnuts: Tuple[Union[PieSeries, XYSeries]] = doughnuts

    @property
    def as_dict(self):
        return self._get_dict({
            "doughnuts": [nut.as_dict for nut in self.doughnuts],
            "type": "doughnut"
        })


class RadarChart(Chart):
    def __init__(self, name: str, *radars: Union[RadarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.radars: Tuple[Union[RadarSeries, XYSeries]] = radars

    @property
    def as_dict(self):
        return self._get_dict({
            "radars": [radar.as_dict for radar in self.radars],
            "type": "radar"
        })


class AreaChart(Chart):
    def __init__(self, name: str, *areas: Union[AreaSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.areas: Tuple[Union[AreaSeries, XYSeries]] = areas

    @property
    def as_dict(self):
        return self._get_dict({
            "areas": [area.as_dict for area in self.areas],
            "type": "area"
        })

class ScatterChart(Chart):
    def __init__(self, name: str, *scatters: Union[ScatterSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.scatters: Tuple[Union[ScatterSeries, XYSeries]] = scatters

    @property
    def as_dict(self):
        return self._get_dict({
            "scatters": [scatter.as_dict for scatter in self.scatters],
            "type": "scatter"
        })

class BubbleChart(Chart):
    def __init__(self, name: str, *bubbles: Union[BubbleSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.bubbles: Tuple[Union[BubbleSeries]] = bubbles

    @property
    def as_dict(self):
        return self._get_dict({
            "bubbles": [bub.as_dict for bub in self.bubbles],
            "type": "bubble"
        })

class StockChart(Chart):
    def __init__(self, name: str, *stocks: Union[StockSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.stocks: Tuple[Union[StockSeries]] = stocks

    @property
    def as_dict(self):
        return self._get_dict({
            "stocks": [stock.as_dict for stock in self.stocks],
            "type": "stock"
        })


def _replace_key_recursive(obj, old_key, new_key):
    for key, value in obj.items():
        if isinstance(value, dict):
            obj[key] = _replace_key_recursive(value, old_key, new_key)
    if old_key in obj:
        obj[new_key] = obj.pop(old_key)
    return obj

class CombinedChart(Chart):
    def __init__(self, name: str, charts: Sequence[Chart], secondaryCharts: Sequence[Chart] = None, options: ChartOptions = None):
        if not options:
            all_options = [chart.options.as_dict for chart in (tuple(charts) + tuple(secondaryCharts)) if chart.options]
            options = {}
            # use reversed() to give the first charts precedence (they overwrite the others)
            for options in reversed(all_options):
                options.update(options)
        
        super().__init__(name, options)
        self.charts = charts
        self.secondaryCharts = secondaryCharts

    def _get_modified_chart_dicts(self):
        primary_list = list(self.charts)
        secondary_list = list(self.secondaryCharts)
        dict_list = []
        for chart in primary_list:
            chart_dict = chart.as_dict
            chart_dict.pop("options", None)
            dict_list.append(chart_dict)
        for chart in secondary_list:
            chart_dict = chart.as_dict
            chart_dict.pop("options", None)
            dict_list.append(_replace_key_recursive(chart_dict, "y", "y2"))
        return dict_list

    @property
    def as_dict(self):
        return self._get_dict({
            "type": "multiple",
            "multiples": self._get_modified_chart_dicts()
        })

class Object(list, Element):
    """# TODO
    """

    def __init__(self, name: str = "", elements: Iterable[Element] = ()):
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
