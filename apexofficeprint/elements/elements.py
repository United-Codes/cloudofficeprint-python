import json
from copy import deepcopy
from typing import Union, Iterable, Mapping, Set, FrozenSet, Dict, List
from abc import abstractmethod, ABC


class CellStyle(ABC):
    """Abstract base class for a cell style
    """
    def __init__(self):
        pass

    def get_dict(self, property_name: str):
        result = {}
        for suffix, value in self._dict_suffixes.items():
            result[property_name + suffix] = value
        return result

    @property
    @abstractmethod
    def _dict_suffixes(self):
        return {}


class CellStyleDocx(CellStyle):
    """Cell styling settings for docx templates"""
    def __init__(self, cell_background_color: str=None, width: Union[int, str]=None):
        super().__init__()
        self.cell_background_color: str = cell_background_color
        self.width: Union[int, str] = width

    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.cell_background_color is not None:
            result['_cell_background_color'] = self.cell_background_color
        if self.width is not None:
            result['_width'] = self.width
        
        return result


class CellStyleXlsx(CellStyle):
    """Cell styling settings for xlsx templates"""
    def __init__(
        self,
        cell_locked: bool=None,
        cell_hidden: bool=None,
        cell_background: str=None,
        font_name: str=None,
        font_size: Union[int, str]=None,
        font_color: str=None,
        font_italic: bool=None,
        font_bold: bool=None,
        font_strike: bool=None,
        font_underline: bool=None,
        font_superscript: bool=None,
        font_subscript: bool=None,
        border_top: str=None,
        border_top_color: str=None,
        border_bottom: str=None,
        border_bottom_color: str=None,
        border_left: str=None,
        border_left_color: str=None,
        border_right: str=None,
        border_right_color: str=None,
        border_diagonal: str=None,
        border_diagonal_direction: str=None,
        border_diagonal_color: str=None,
        text_h_alignment: str=None,
        text_v_alignment: str=None,
        text_rotation: Union[int, str]=None
    ):
        super().__init__()
        self.cell_locked: bool = cell_locked
        self.cell_hidden: bool = cell_hidden
        self.cell_background: str = cell_background
        """hex color e.g: #ff0000"""
        self.font_name: str = font_name
        """name of the font e.g: Arial"""
        self.font_size: Union[int, str] = font_size
        self.font_color: str = font_color
        """hex color e.g: #00ff00"""
        self.font_italic: bool = font_italic
        self.font_bold: bool = font_bold
        self.font_strike: bool = font_strike
        self.font_underline: bool = font_underline
        self.font_superscript: bool = font_superscript
        self.font_subscript: bool = font_subscript
        self.border_top: str = border_top
        """[dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]"""
        self.border_top_color: str = border_top_color
        """hex color e.g: #000000"""
        self.border_bottom: str = border_bottom
        """[dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]"""
        self.border_bottom_color: str = border_bottom_color
        """hex color e.g: #000000"""
        self.border_left: str = border_left
        """[dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]"""
        self.border_left_color: str = border_left_color
        """hex color e.g: #000000"""
        self.border_right: str = border_right
        """[dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]"""
        self.border_right_color: str = border_right_color
        """hex color e.g: #000000"""
        self.border_diagonal: str = border_diagonal
        """[dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]"""
        self.border_diagonal_direction: str = border_diagonal_direction
        """[up-wards|down-wards| both]"""
        self.border_diagonal_color: str = border_diagonal_color
        """hex color e.g: #000000"""
        self.text_h_alignment: str = text_h_alignment
        """[top|bottom|center|justify]"""
        self.text_v_alignment: str = text_v_alignment
        """[top|bottom|center|justify]"""
        self.text_rotation: Union[int, str] = text_rotation
        """rotation of text value from 0-90 degrees"""

    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.cell_locked is not None:
            result['_cell_locked'] = self.cell_locked
        if self.cell_hidden is not None:
            result['_cell_hidden'] = self.cell_hidden
        if self.cell_background is not None:
            result['_cell_background'] = self.cell_background
        if self.font_name is not None:
            result['_font_name'] = self.font_name
        if self.font_size is not None:
            result['_font_size'] = self.font_size
        if self.font_color is not None:
            result['_font_color'] = self.font_color
        if self.font_italic is not None:
            result['_font_italic'] = self.font_italic
        if self.font_bold is not None:
            result['_font_bold'] = self.font_bold
        if self.font_strike is not None:
            result['_font_strike'] = self.font_strike
        if self.font_underline is not None:
            result['_font_underline'] = self.font_underline
        if self.font_superscript is not None:
            result['_font_superscript'] = self.font_superscript
        if self.font_subscript is not None:
            result['_font_subscript'] = self.font_subscript
        if self.border_top is not None:
            result['_border_top'] = self.border_top
        if self.border_top_color is not None:
            result['_border_top_color'] = self.border_top_color
        if self.border_bottom is not None:
            result['_border_bottom'] = self.border_bottom
        if self.border_bottom_color is not None:
            result['_border_bottom_color'] = self.border_bottom_color
        if self.border_left is not None:
            result['_border_left'] = self.border_left
        if self.border_left_color is not None:
            result['_border_left_color'] = self.border_left_color
        if self.border_right is not None:
            result['_border_right'] = self.border_right
        if self.border_right_color is not None:
            result['_border_right_color'] = self.border_right_color
        if self.border_diagonal is not None:
            result['_border_diagonal'] = self.border_diagonal
        if self.border_diagonal_direction is not None:
            result['_border_diagonal_direction'] = self.border_diagonal_direction
        if self.border_diagonal_color is not None:
            result['_border_diagonal_color'] = self.border_diagonal_color
        if self.text_h_alignment is not None:
            result['_text_h_alignment'] = self.text_h_alignment
        if self.text_v_alignment is not None:
            result['_text_v_alignment'] = self.text_v_alignment
        if self.text_rotation is not None:
            result['_text_rotation'] = self.text_rotation
        
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
        """JSON representation of this `Element`.

        Isomorphic with the dict representation (`Element.as_dict`).

        Returns:
            str: JSON representation
        """
        return json.dumps(self.as_dict)

    @property
    @abstractmethod
    def as_dict(self) -> Dict:
        """Dictionary representation of this `Element`.

        Isomorphic with the JSON representation (`Element.json`).

        Returns:
            Dict: dictionary representation
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
    def as_dict(self) -> Dict:
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

        if self.color is not None:
            result[self.name + "_color"] = self.color
        if self.font is not None:
            result[self.name + "_font"] = self.font
        if self.width is not None:
            result[self.name + "_width"] = self.width
        if self.height is not None:
            result[self.name + "_height"] = self.height
        if self.opacity is not None:
            result[self.name + "_opacity"] = self.opacity
        if self.rotation is not None:
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
    def as_dict(self) -> Dict:
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


class PageBreak(Property):
    """Value should be set to 'page' or 'pagebreak' for PageBreak, 'column' or 'columnbreak' for column breaks,
    if set to True (default) it will create a pagebreak."""
    def __init__(self, name: str, value: Union[str, bool]):
        super().__init__(name, value)
    
    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?" + self.name + "}"})


class MarkdownContent(Property):
    """Value holds the Markdown content"""
    def __init__(self, name: str, value: str):
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{_" + self.name + "_}"})


class TextBox(Element):
    """This tag will allow you to insert a text box starting in the cell containing the tag in Excel."""
    def __init__(self,
    name: str,
    value: str,
    font: str=None,
    font_color: str=None,
    font_size: Union[int, str]=None,
    transparency: Union[int, str]=None,
    width: Union[int, str]=None,
    height: Union[int, str]=None):
        super().__init__(name)
        self.value: str = value
        self.font: str = font
        self.font_color: str = font_color
        self.font_size: Union[int, str] = font_size
        self.transparency: Union[int, str] = transparency
        self.width: Union[int, str] = width
        self.height: Union[int, str] = height
    
    @property
    def available_tags(self):
        return frozenset({"{tbox " + self.name + "}"})

    @property
    def as_dict(self):
        result = {
            self.name: self.value
        }

        if self.font is not None:
            result[self.name + '_font'] = self.font
        if self.font_color is not None:
            result[self.name + '_font_color'] = self.font_color
        if self.font_size is not None:
            result[self.name + '_font_size'] = self.font_size
        if self.transparency is not None:
            result[self.name + '_transparency'] = self.transparency
        if self.width is not None:
            result[self.name + '_width'] = self.width
        if self.height is not None:
            result[self.name + '_height'] = self.height

        return result


class ElementCollection(list, Element):
    """A collection used to group multiple elements together.
    It can contain nested `ElementCollection`s and should be used to pass multiple `Element`s as PrintJob data, as well as to allow for nested elements.
    Its name is used as a key name when nested, but ignored for all purposes when it's the outer ElementCollection.
    """
    def __init__(self, name: str = "", elements: Iterable[Element] = ()):
        # name is not used for the outer ElementCollection, but needed for nested ElementCollections
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

    def add_all(self, obj: 'ElementCollection'):
        for element in obj:
            self.add(element)

    def remove_element_by_name(self, element_name: str):
        self.remove(
            next(element for element in self if element.name == element_name)
        )

    @property
    def as_dict(self) -> Dict:
        """Merge the `ElementCollection`'s contents as one dict.

        Returns:
            Dict: merged element
        """
        result = {}
        for element in self:
            if isinstance(element, ElementCollection):
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
    def element_to_element_collection(cls, element: Element, name: str = "") -> 'ElementCollection':
        return cls.from_mapping(element.as_dict, name)

    @classmethod
    def from_mapping(cls, mapping: Mapping, name: str = "") -> 'ElementCollection':
        result_set = set()
        for key, value in mapping.items():
            result_set.add(Property(key, value))
        return cls(name, result_set)

    @classmethod
    def from_json(cls, json_str: str, name: str = "") -> 'ElementCollection':
        return cls.from_mapping(json.loads(json_str), name)
