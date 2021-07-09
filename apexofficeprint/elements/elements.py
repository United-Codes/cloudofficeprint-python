import json
from copy import deepcopy
from typing import Union, Iterable, Mapping, Set, FrozenSet, Dict, List
from abc import abstractmethod, ABC


class CellStyle:
    def __init__(self, background_color: str = None, width: Union[str, int] = None):
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
    def as_dict(self) -> dict:
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


class Hyperlink(Element):
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
        """Title of the table of contents. Default is 'Contents'"""
        self.depth: int = depth
        """The depth of heading to be shown, default 3"""
        self.tab_leader: str = tab_leader
        """How the space between title and page number should be filled. Can be "hyphen", "underscore", or "dot" (default)."""

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
                 highlight_color: str = None):
        super().__init__(name, value)
        self.font: str = font
        self.font_size: Union[str, int] = font_size
        self.font_color: str = font_color
        self.bold: bool = bold
        self.italic: bool = italic
        self.underline: bool = underline
        self.strikethrough: bool = strikethrough
        self.highlight_color: str = highlight_color

    @property
    def available_tags(self):
        return frozenset({"{style " + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        if self.font is not None:
            result[self.name + "_font_family"] = self.font
        if self.font_size is not None:
            result[self.name + "_font_size"] = self.font_size
        if self.font_color is not None:
            result[self.name + "_font_color"] = self.font_color
        if self.bold is not None:
            result[self.name + "_bold"] = self.bold
        if self.italic is not None:
            result[self.name + "_italic"] = self.italic
        if self.underline is not None:
            result[self.name + "_underline"] = self.underline
        if self.strikethrough is not None:
            result[self.name + "_strikethrough"] = self.strikethrough
        if self.highlight_color is not None:
            result[self.name + "_highlight"] = self.highlight_color

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
        self.color: str = color
        self.font: str = font
        self.width: Union[int, str] = width
        self.height: Union[int, str] = height
        self.opacity: float = opacity
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


class D3Code(Element):
    def __init__(self, name: str, code: str, data=None):
        super().__init__(name)
        self.code: str = code
        self.data = data
        """The data that the code will have access to"""

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$d3 " + self.name + "}"})
    
    @property
    def as_dict(self):
        result = {
            self.name: self.code
        }

        if self.data is not None:
            result[self.name + '_data'] = self.data
        
        return result

class AOPChartDateOptions:
    """Date options for an AOPChart (different from ChartDateOptions in charts.py)."""
    def __init__(self,
                 format: str = None,
                 unit: str = None,
                 step: Union[int, str] = None):
        self.format: str = format
        """The format to display the date on the chart's axis."""
        self.unit: str = unit
        """The unit to be used for spacing the axis values."""
        self.step: Union[int, str] = step
        """how many of the above unit should be used for spacing the axis values (automatic if undefined). 
        This option is not supported in LibreOffice."""

    @property
    def as_dict(self):
        result = {}

        if self.format is not None:
            result["format"] = self.format
        if self.unit is not None:
            result["unit"] = self.unit
        if self.step is not None:
            result["step"] = self.step

        return result


class AOPChart(Element):
    def __init__(self,
                 name: str,
                 x_data: Iterable,
                 y_datas: Union[Iterable[Iterable], Mapping[str, Iterable]],
                 date: AOPChartDateOptions = None,
                 title: str = None,
                 x_title: str = None,
                 y_title: str = None,
                 y2_title: str = None,
                 x2_title: str = None):
        super().__init__(name)
        self.x_data: List = list(x_data)

        self.y_datas: Dict[str, Iterable[Union[str, int, float]]] = None
        """If the argument 'y_datas' is of type Iterable[Iterable], then default names (e.g. series 1, series 2, ...) will be used."""
        if isinstance(y_datas, Mapping):
            self.y_datas = {
                name: list(data) for name, data in y_datas.items()
            }
        elif isinstance(y_datas, Iterable):
            self.y_datas = {
                f"series {i+1}": list(data) for i, data in enumerate(y_datas)
            }
        else:
            raise TypeError(
                f'Expected Mapping or Iterable for y_data, got "{type(y_datas)}"')

        self.date: AOPChartDateOptions = date
        self.title: str = title
        self.x_title: str = x_title
        self.y_title: str = y_title
        self.x2_title: str = x2_title
        self.y2_title: str = y2_title

    @classmethod
    def from_dataframe(cls,
                       name: str,
                       data: 'pandas.DataFrame',
                       date: AOPChartDateOptions = None,
                       title: str = None,
                       x_title: str = None,
                       y_title: str = None,
                       y2_title: str = None,
                       x2_title: str = None):
        x_data = list(data.iloc[:, 0])

        y_frame = data.iloc[:, 1:]
        y_datas = {}
        for col_name, col_data in y_frame.iteritems():
            y_datas[col_name] = col_data

        return cls(name, x_data, y_datas, date, title, x_title, y_title, y2_title, x2_title)

    @property
    def as_dict(self) -> dict:
        result = {
            "xAxis": {
                "data": self.x_data,
            },
            "yAxis": {
                "series": [{
                    "name": name,
                    "data": data
                } for name, data in self.y_datas.items()]
            }
        }

        if self.title is not None:
            result["title"] = self.title
        if self.date is not None:
            result['xAxis']['date'] = self.date.as_dict
        if self.x_title is not None:
            result["xAxis"]["title"] = self.x_title
        if self.y_title is not None:
            result["yAxis"]["title"] = self.y_title
        if self.x2_title is not None:
            result['x2Axis'] = {}
            result["x2Axis"]["title"] = self.x2_title
        if self.y2_title is not None:
            result['y2Axis'] = {}
            result["y2Axis"]["title"] = self.y2_title

        return {self.name: result}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{aopchart " + self.name + "}"})


class Object(list, Element):
    """A collection used to group multiple elements together.
    It can contain nested `Object`s and should be used to pass multiple `Element`s as PrintJob data, as well as to allow for nested elements.
    Its name is used as a key name when nested, but ignored for all purposes when it's the outer object.
    """
    def __init__(self, name: str = "", elements: Iterable[Element] = ()):
        # name is not used for the outer object, but needed for nested objects
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

    # The reason we use 'Object' (a string) in cases like this is that
    # Object is actually a forward reference here,
    # which doesn't work, the interpreter will have no idea what Object is.
    # It is supposed to work out of the box in future Python (>= 3.10)
    # and with >= 3.7 using "from __future__ import annotations"
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
            if isinstance(element, Object):
                result.update({element.name: element.as_dict})
            else:
                result.update(element.as_dict)
        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        result = set()
        for element in self:
            result |= element.available_tags
        return frozenset(result)

    @classmethod
    def element_to_object(cls, element: Element, name: str = "") -> 'Object':
        return cls.from_mapping(element.as_dict, name)

    @classmethod
    def from_mapping(cls, mapping: Mapping, name: str = "") -> 'Object':
        result_set = set()
        for key, value in mapping.items():
            result_set.add(Property(key, value))
        return cls(name, result_set)

    @classmethod
    def from_json(cls, json_str: str, name: str = "") -> 'Object':
        return cls.from_mapping(json.loads(json_str), name)
