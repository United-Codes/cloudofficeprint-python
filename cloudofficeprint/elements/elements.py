import json
from copy import deepcopy
from typing import Any, Union, Iterable, Mapping, Set, FrozenSet, Dict, List
from abc import abstractmethod, ABC
import pandas


class CellStyle(ABC):
    """Abstract base class for a cell style"""

    def __init__(self):
        pass

    def get_dict(self, property_name: str) -> Dict:
        """Get the dict representation of this cell style.

        Args:
            property_name (str): The name of the property for which you want to define the cell style

        Returns:
            Dict: dict representation of this cell style
        """
        result = {}
        for suffix, value in self._dict_suffixes.items():
            result[property_name + suffix] = value
        return result

    @property
    @abstractmethod
    def _dict_suffixes(self) -> Dict:
        """Get the dict representation of the suffixes that need to be appended to the name of this property in this CellStyle object's dict representation.

        Returns:
            Dict: the dict representation of the suffixes that need to be appended to the name of this property in this CellStyle object's dict representation
        """
        return {}


class CellStyleDocx(CellStyle):
    """Cell styling settings for docx templates"""

    def __init__(
        self, 
        cell_background_color: str = None, 
        width: Union[int, str] = None, 
        preserve_total_width_of_table: str = None,
        border: str = None,
        border_top: str = None,
        border_bottom: str = None,
        border_left: str = None,
        border_right: str = None,
        border_diagonal_down: str = None,
        border_diagonal_up: str = None,
        border_color: str = None,
        border_top_color: str = None,
        border_bottom_color: str = None,
        border_left_color: str = None,
        border_right_color: str = None,
        border_diagonal_up_color: str = None,
        border_diagonal_down_color: str = None,
        border_size:  Union[int, str] = None,
        border_top_size:  Union[int, str] = None,
        border_bottom_size:  Union[int, str] = None,
        border_left_size:  Union[int, str] = None,
        border_right_size:  Union[int, str] = None,
        border_diagonal_up_size:  Union[int, str] = None,
        border_diagonal_down_size:  Union[int, str] = None,
        border_space:  Union[int, str] = None,
        border_top_space:  Union[int, str] = None,
        border_bottom_space:  Union[int, str] = None,
        border_left_space:  Union[int, str] = None,
        border_right_space:  Union[int, str] = None,
        border_diagonal_up_space:  Union[int, str] = None,
        border_diagonal_down_space:  Union[int, str] = None,    
    ):
        """
        Args:
            cell_background_color (str, optional): The background color of the cell. Defaults to None.
            width (Union[int, str], optional): The width of the cell. Defaults to None.
            preserve_total_width_of_table (str, optional): Keeps table width constant by redistributing removed column's width to others.
            border (str, optional): Applies the specified border style to all table edges (top, bottom, left, right).
            border_top (str, optional): Applies the specified border style to the top edge of the table.
            border_bottom (str, optional): Applies the specified border style to the bottom edge of the table.
            border_left (str, optional): Applies the specified border style to the left edge of the table.
            border_right (str, optional): Applies the specified border style to the right edge of the table.
            border_diagonal_down (str, optional): Applies the specified border style to the diagonal line going from the top-left to the bottom-right corner.
            border_diagonal_up (str, optional): Applies the specified border style to the diagonal line going from the bottom-left to the top-right corner.
            border_color (str, optional): Sets the color of the borders (top, bottom, left, right).
            border_top_color (str, optional): Sets the color of the top border.
            border_bottom_color (str, optional): Sets the color of the bottom border.
            border_left_color (str, optional): Sets the color of the left border.
            border_right_color (str, optional): Sets the color of the right border.
            border_diagonal_up_color (str, optional): Sets the color of the diagonal up border.
            border_diagonal_down_color (str, optional): Sets the color of the diagonal down border.
            border_size (Union[int, str], optional): Sets the width of the borders (top, bottom, left, right) in points.
            border_top_size (Union[int, str], optional): Sets the width of the top border in points.
            border_bottom_size (Union[int, str], optional): Sets the width of the bottom border in points.
            border_left_size (Union[int, str], optional): Sets the width of the left border in points.
            border_right_size (Union[int, str], optional): Sets the width of the right border in points.
            border_diagonal_up_size (Union[int, str], optional): Sets the width of the diagonal up border in points.
            border_diagonal_down_size (Union[int, str], optional): Sets the width of the diagonal down border in points.
            border_space (Union[int, str], optional): Sets the spacing between the content and borders (top, bottom, left, right) in points.
            border_top_space (Union[int, str], optional): Sets the spacing between the content and the top border in points.
            border_bottom_space (Union[int, str], optional): Sets the spacing between the content and the bottom border in points.
            border_left_space (Union[int, str], optional): Sets the spacing between the content and the left border in points.
            border_right_space (Union[int, str], optional): Sets the spacing between the content and the right border in points.
            border_diagonal_up_space (Union[int, str], optional): Sets the spacing between the content and the diagonal up border in points.
            border_diagonal_down_space (Union[int, str], optional): Sets the spacing between the content and the diagonal down border in points.
        """
        super().__init__()
        self.cell_background_color: str = cell_background_color
        self.width: Union[int, str] = width
        self.preserve_total_width_of_table: str = preserve_total_width_of_table
        self.border: str = border
        self.border_top: str = border_top
        self.border_bottom: str = border_bottom
        self.border_left: str = border_left
        self.border_right: str = border_right
        self.border_diagonal_down: str = border_diagonal_down
        self.border_diagonal_up: str = border_diagonal_up
        self.border_color: str = border_color
        self.border_top_color: str = border_top_color
        self.border_bottom_color: str = border_bottom_color
        self.border_left_color: str = border_left_color
        self.border_right_color: str = border_right_color
        self.border_diagonal_up_color: str = border_diagonal_up_color
        self.border_diagonal_down_color: str = border_diagonal_down_color
        self.border_size: Union[int, str] = border_size
        self.border_top_size: Union[int, str] = border_top_size
        self.border_bottom_size: Union[int, str] = border_bottom_size
        self.border_left_size: Union[int, str] = border_left_size
        self.border_right_size: Union[int, str] = border_right_size
        self.border_diagonal_up_size: Union[int, str] = border_diagonal_up_size
        self.border_diagonal_down_size: Union[int, str] = border_diagonal_down_size
        self.border_space: Union[int, str] = border_space
        self.border_top_space: Union[int, str] = border_top_space
        self.border_bottom_space: Union[int, str] = border_bottom_space
        self.border_left_space: Union[int, str] = border_left_space
        self.border_right_space: Union[int, str] = border_right_space
        self.border_diagonal_up_space: Union[int, str] = border_diagonal_up_space
        self.border_diagonal_down_space: Union[int, str] = border_diagonal_down_space
        
    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes
        if self.cell_background_color is not None:
            result["_cell_background_color"] = self.cell_background_color
        if self.width is not None:
            result["_width"] = self.width
        if self.preserve_total_width_of_table is not None:
            result["_preserve_total_width_of_table"] = self.preserve_total_width_of_table
        if self.border is not None:
            result["_border"] = self.border
        if self.border_top is not None:
            result["_border_top"] = self.border_top
        if self.border_bottom is not None:
            result["_border_bottom"] = self.border_bottom
        if self.border_left is not None:
            result["_border_left"] = self.border_left
        if self.border_right is not None:
            result["_border_right"] = self.border_right
        if self.border_diagonal_down is not None:
            result["_border_diagonal_down"] = self.border_diagonal_down
        if self.border_diagonal_up is not None:
            result["_border_diagonal_up"] = self.border_diagonal_up
        if self.border_color is not None:
            result["_border_color"] = self.border_color
        if self.border_top_color is not None:
            result["_border_top_color"] = self.border_top_color
        if self.border_bottom_color is not None:
            result["_border_bottom_color"] = self.border_bottom_color
        if self.border_left_color is not None:
            result["_border_left_color"] = self.border_left_color
        if self.border_right_color is not None:
            result["_border_right_color"] = self.border_right_color
        if self.border_diagonal_up_color is not None:
            result["_border_diagonal_up_color"] = self.border_diagonal_up_color
        if self.border_diagonal_down_color is not None:
            result["_border_diagonal_down_color"] = self.border_diagonal_down_color
        if self.border_size is not None:
            result["_border_size"] = self.border_size
        if self.border_top_size is not None:
            result["_border_top_size"] = self.border_top_size
        if self.border_bottom_size is not None:
            result["_border_bottom_size"] = self.border_bottom_size
        if self.border_left_size is not None:
            result["_border_left_size"] = self.border_left_size
        if self.border_right_size is not None:
            result["_border_right_size"] = self.border_right_size
        if self.border_diagonal_up_size is not None:
            result["_border_diagonal_up_size"] = self.border_diagonal_up_size
        if self.border_diagonal_down_size is not None:
            result["_border_diagonal_down_size"] = self.border_diagonal_down_size
        if self.border_space is not None:
            result["_border_space"] = self.border_space
        if self.border_top_space is not None:
            result["_border_top_space"] = self.border_top_space
        if self.border_bottom_space is not None:
            result["_border_bottom_space"] = self.border_bottom_space
        if self.border_left_space is not None:
            result["_border_left_space"] = self.border_left_space
        if self.border_right_space is not None:
            result["_border_right_space"] = self.border_right_space
        if self.border_diagonal_up_space is not None:
            result["_border_diagonal_up_space"] = self.border_diagonal_up_space
        if self.border_diagonal_down_space is not None:
            result["_border_diagonal_down_space"] = self.border_diagonal_down_space
        return result


class CellStyleXlsx(CellStyle):
    """Cell styling settings for xlsx templates"""

    def __init__(
        self,
        cell_locked: bool = None,
        cell_hidden: bool = None,
        cell_background: str = None,
        font_name: str = None,
        font_size: Union[int, str] = None,
        font_color: str = None,
        font_italic: bool = None,
        font_bold: bool = None,
        font_strike: bool = None,
        font_underline: bool = None,
        font_superscript: bool = None,
        font_subscript: bool = None,
        border_top: str = None,
        border_top_color: str = None,
        border_bottom: str = None,
        border_bottom_color: str = None,
        border_left: str = None,
        border_left_color: str = None,
        border_right: str = None,
        border_right_color: str = None,
        border_diagonal: str = None,
        border_diagonal_direction: str = None,
        border_diagonal_color: str = None,
        text_h_alignment: str = None,
        text_v_alignment: str = None,
        text_rotation: Union[int, str] = None,
        wrap_text: bool = False,
        width: Union[int, str] = None,
        height: Union[int, str] = None,
        max_characters : Union[int, str] = None,
        height_scaling : Union[int, str] = None,
    ):
        """
        Args:
            cell_locked (bool, optional): Whether or not the cell is locked. Defaults to None.
            cell_hidden (bool, optional): Whether or not the cell is hidden. Defaults to None.
            cell_background (str, optional): hex color e.g: #ff0000. Defaults to None.
            font_name (str, optional): name of the font e.g: Arial. Defaults to None.
            font_size (Union[int, str], optional): The size of the font. Defaults to None.
            font_color (str, optional): hex color e.g: #00ff00. Defaults to None.
            font_italic (bool, optional): Whether or not the text is in italic. Defaults to None.
            font_bold (bool, optional): Whether or not the text is in bold. Defaults to None.
            font_strike (bool, optional): Whether or not the text is struck. Defaults to None.
            font_underline (bool, optional): Whether or not the text is underlined. Defaults to None.
            font_superscript (bool, optional): Whether or not the text is in superscript. Defaults to None.
            font_subscript (bool, optional): Whether or not the text is in subscript. Defaults to None.
            border_top (str, optional): [dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]. Defaults to None.
            border_top_color (str, optional): hex color e.g: #000000. Defaults to None.
            border_bottom (str, optional): [dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]. Defaults to None.
            border_bottom_color (str, optional): hex color e.g: #000000. Defaults to None.
            border_left (str, optional): [dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]. Defaults to None.
            border_left_color (str, optional): hex color e.g: #000000. Defaults to None.
            border_right (str, optional): [dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]. Defaults to None.
            border_right_color (str, optional): hex color e.g: #000000. Defaults to None.
            border_diagonal (str, optional): [dashed / dashDot / hair / dashDotDot / dotted / mediumDashDot / mediumDashed / mediumDashDotDot / slantDashDot / medium / double / thick ]. Defaults to None.
            border_diagonal_direction (str, optional): [up-wards|down-wards| both]. Defaults to None.
            border_diagonal_color (str, optional): hex color e.g: #000000. Defaults to None.
            text_h_alignment (str, optional): [top|bottom|center|justify]. Defaults to None.
            text_v_alignment (str, optional): [top|bottom|center|justify]. Defaults to None.
            text_rotation (Union[int, str], optional): Rotation of text value from 0-90 degrees. Defaults to None.
            wrap_text (bool, optional): Set to true for wrap text. When false (default )S,the property won't be included in the output.
            width (Union[int, str],  optional): Provide a custom width to the cell. Supported units: inch, cm, px, pt, em, Excel Units(eu)
            height (Union[int, str],  optional): Provide custom height to the cell. Supported units: inch, cm, px, pt, em, Excel Units(eu)
            max_characters (Union[int, str],  optional): Provide width for the cell.
            height_scaling (Union[int, str], optional):  Adjusts cell height for consistent rendering.
        """
        super().__init__()
        self.cell_locked: bool = cell_locked
        self.cell_hidden: bool = cell_hidden
        self.cell_background: str = cell_background
        self.font_name: str = font_name
        self.font_size: Union[int, str] = font_size
        self.font_color: str = font_color
        self.font_italic: bool = font_italic
        self.font_bold: bool = font_bold
        self.font_strike: bool = font_strike
        self.font_underline: bool = font_underline
        self.font_superscript: bool = font_superscript
        self.font_subscript: bool = font_subscript
        self.border_top: str = border_top
        self.border_top_color: str = border_top_color
        self.border_bottom: str = border_bottom
        self.border_bottom_color: str = border_bottom_color
        self.border_left: str = border_left
        self.border_left_color: str = border_left_color
        self.border_right: str = border_right
        self.border_right_color: str = border_right_color
        self.border_diagonal: str = border_diagonal
        self.border_diagonal_direction: str = border_diagonal_direction
        self.border_diagonal_color: str = border_diagonal_color
        self.text_h_alignment: str = text_h_alignment
        self.text_v_alignment: str = text_v_alignment
        self.text_rotation: Union[int, str] = text_rotation
        self.wrap_text: bool = wrap_text
        self.width: Union[int, str] = width
        self.height: Union[int, str] = height
        self.max_characters: Union[int, str] = max_characters 
        self.height_scaling: Union[int, str] = height_scaling
        
        
        

    @property
    def _dict_suffixes(self):
        result = super()._dict_suffixes

        if self.cell_locked is not None:
            result["_cell_locked"] = self.cell_locked
        if self.cell_hidden is not None:
            result["_cell_hidden"] = self.cell_hidden
        if self.cell_background is not None:
            result["_cell_background"] = self.cell_background
        if self.font_name is not None:
            result["_font_name"] = self.font_name
        if self.font_size is not None:
            result["_font_size"] = self.font_size
        if self.font_color is not None:
            result["_font_color"] = self.font_color
        if self.font_italic is not None:
            result["_font_italic"] = self.font_italic
        if self.font_bold is not None:
            result["_font_bold"] = self.font_bold
        if self.font_strike is not None:
            result["_font_strike"] = self.font_strike
        if self.font_underline is not None:
            result["_font_underline"] = self.font_underline
        if self.font_superscript is not None:
            result["_font_superscript"] = self.font_superscript
        if self.font_subscript is not None:
            result["_font_subscript"] = self.font_subscript
        if self.border_top is not None:
            result["_border_top"] = self.border_top
        if self.border_top_color is not None:
            result["_border_top_color"] = self.border_top_color
        if self.border_bottom is not None:
            result["_border_bottom"] = self.border_bottom
        if self.border_bottom_color is not None:
            result["_border_bottom_color"] = self.border_bottom_color
        if self.border_left is not None:
            result["_border_left"] = self.border_left
        if self.border_left_color is not None:
            result["_border_left_color"] = self.border_left_color
        if self.border_right is not None:
            result["_border_right"] = self.border_right
        if self.border_right_color is not None:
            result["_border_right_color"] = self.border_right_color
        if self.border_diagonal is not None:
            result["_border_diagonal"] = self.border_diagonal
        if self.border_diagonal_direction is not None:
            result["_border_diagonal_direction"] = self.border_diagonal_direction
        if self.border_diagonal_color is not None:
            result["_border_diagonal_color"] = self.border_diagonal_color
        if self.text_h_alignment is not None:
            result["_text_h_alignment"] = self.text_h_alignment
        if self.text_v_alignment is not None:
            result["_text_v_alignment"] = self.text_v_alignment
        if self.text_rotation is not None:
            result["_text_rotation"] = self.text_rotation
        if self.wrap_text is True:
            result["_wrap_text"] = self.wrap_text
        if self.width is not None:
            result["_width"] = self.width
        if self.height is not None:
            result["_height"] = self.height
        if self.max_characters is not None:
            result["_max_characters"] = self.max_characters
        if self.height_scaling is not None:
            result["_height_scaling"] = self.height_scaling

        return result


class Element(ABC):
    """The abstract base class for elements."""

    def __init__(self, name: str):
        """
        Args:
            name (str): The name of this element.
        """
        self.name = name

    def __str__(self) -> str:
        """Get the string representation of this object.

        Returns:
            str: string representation of this object
        """
        return self.json

    def __repr__(self) -> str:
        """Get the JSON representation of this object.

        Returns:
            str: JSON representation of this object
        """
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
        """
        Args:
            name (str): The name for this property.
            value (str): The value for this property. Note: the general purpose for this value-field is the value as a string,
                but this can be of any type, for example a dict.
        """
        super().__init__(name)
        self.value: Union[int, str] = value

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        return {self.name: self.value}


class CellStyleProperty(Property):
    def __init__(self, name: str, value: str, cell_style: CellStyle):
        """
        Args:
            name (str): The name for this property
            value (str): The value for this property
            cell_style (CellStyle): Cell style as a `CellStyle`.
        """
        super().__init__(name, value)
        self.cell_style: CellStyle = cell_style

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "$}"})

    @property
    def as_dict(self) -> Dict:
        result = {self.name: self.value}

        for suffix, value in self.cell_style._dict_suffixes.items():
            result[self.name + suffix] = value

        return result


class Html(Property):
    def __init__(
        self, name: str,
        value: str, 
        custom_table_style: str, 
        unordered_list_style: Union[str, int], 
        ordered_list_style: Union[str, int], 
        use_tag_style: bool, 
        ignore_cell_margin: bool, 
        ignore_empty_p: bool
    ):
        """
        Args:
            name (str): The name for this property.
            value (str): The value for this property.
            custom_table_style (str): Specify custom table style
            unordered_list_style (str): Create and customize ordered list
            ordered_list_style (str): Create and customize unordered list
            use_tag_style (bool): Use the styling from the template instead of default Word styling
            ignore_cell_margin (bool):  Ignore empty paragraphs within HTML content
            ignore_empty_p (bool):  Ignore the cell margins in an HTML table cell when the text content is large
        """
        super().__init__(name, value)
        self.custom_table_style: str = custom_table_style
        self.unordered_list_style: Union[str, int] = unordered_list_style
        self.ordered_list_style: Union[str, int] = ordered_list_style
        self.use_tag_style: bool = use_tag_style
        self.ignore_cell_margin: bool = ignore_cell_margin
        self.ignore_empty_p: bool = ignore_empty_p
       
    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{_" + self.name + "}"})
    
    @property
    def as_dict(self) -> Dict:
        result = {self.name: self.value}

        if self.custom_table_style is not None:
            result[self.name + "_custom_table_style"] = self.custom_table_style
        if self.unordered_list_style is not None:
            result[self.name + "_unordered_list_style"] = self.unordered_list_style
        if self.ordered_list_style is not None:
            result[self.name + "_ordered_list_style"] = self.ordered_list_style
        if self.use_tag_style is not None:
            result[self.name + "_use_tag_style"] = self.use_tag_style
        if self.ignore_cell_margin is not None:
            result[self.name + "_ignore_cell_margin"] = self.ignore_cell_margin
        if self.ignore_empty_p is not None:
            result[self.name + "_ignore_empty_p"] = self.ignore_empty_p
        return result

class RightToLeft(Property):
    def __init__(self, name: str, value: str):
        """
        Args:
            name (str): The name for this property.
            value (str): The value for this property.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{<" + self.name + "}"})


class FootNote(Property):
    def __init__(self, name: str, value: str):
        """
        Args:
            name (str): The name for this property.
            value (str): The value for this property.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{+" + self.name + "}"})


class AutoLink(Property):
    """ This tag allows you to insert text into the document detecting links.
       For PPTX templates, additional styling options are available including:
    - Custom font color for hyperlinks
    - Custom underline color
    - Option to preserve template styling
    """

    def __init__(self, 
                 name: str, 
                 value: str,
                 font_color: Union[str, None] = None,
                 underline_color: Union[str, None] = None,
                 preserve_tag_style: Union[bool, str, None] = None):
        """
        Args:
            name (str): The name for this element.
            value (str): The value of the autoLink.
            font_color (str, optional): PPTX-only The font color of autolink.
            underline_color (str, optional): The underline color of autolink.
            preserve_tag_style (str or bool, optional): Take the styling of hyperlink text defined in the template (blue and underlined by default).
        """
        super().__init__(name, value)
        self.value: str = value
        self.font_color = font_color
        self.underline_color = underline_color
        self.preserve_tag_style = preserve_tag_style

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{*auto " + self.name + "}"})
    @property
    def as_dict(self) -> Dict :
        result ={self.name:self.value}
        if self.font_color is not None:
            result[f"{self.name}_font_color"] = self.font_color
        if self.underline_color is not None:
            result[f"{self.name}_underline_color"] = self.underline_color
        if self.preserve_tag_style is not None:
            result[f"{self.name}_preserve_tag_style"] = self.preserve_tag_style
        return result
    
class Hyperlink(Element):
    def __init__(self, name: str, url: str, text: str = None):
        """
        Args:
            name (str): The name for this element.
            url (str): The URL for the hyperlink.
            text (str, optional): The text for the hyperlink. Defaults to None.
            font_color (str, optional): PPTX ONLY -The font color of text for hyperlink. ( optional)
            underline_color (str, optional): PPTX ONLY -The underline color of text for hyperlink. ( optional)
            preserve_tag_style (str or bool, optional): For PPTX & Word- Take the styling of hyperlink text defined in the template (blue and underlined by default). ( optional)
        """
        super().__init__(name)
        self.url: str = url
        self.text: Union[str, None] = None
        self.font_color: Union[str, None] = None
        self.underline_color: Union[str, None] = None
        self.preserve_tag_style: Union[str, bool, None] = None

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{*" + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        result = {self.name: self.url}

        if self.text is not None:
            result[self.name + "_text"] = self.text
        if  (self.text is not None) and (self.font_color is not None):
            result[self.text + "_font_color"] = self.font_color
        if (self.text is not None) and (self.underline_color is not None):
            result[self.text + "_underline_color"] = self.underline_color
        if (self.preserve_tag_style is not None):
            result[self.name + "_preserve_tag_style"] = self.preserve_tag_style

        return result
class TableOfContents(Element):
    def __init__(
        self, name: str, title: str = None, depth: int = None, tab_leader: str = None
    ):
        """
        Args:
            name (str): The name for this element.
            title (str): Title of the table of contents. Defaults to None.
            depth (int, optional): The depth of heading to be shown, default 3. Defaults to None.
            tab_leader (str, optional): How the space between title and page number should be filled. Can be "hyphen", "underscore", or "dot" (default). Defaults to None.
        """
        super().__init__(name)
        self.title: str = title
        self.depth: int = depth
        self.tab_leader: str = tab_leader

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{~" + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
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
        """
        Args:
            name (str): The name for this property.
            value (str): The value for this property.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{@" + self.name + "}"})


class Span(Property):
    def __init__(self, name: str, value: str, columns: int, rows: int):
        """
        Args:
            name (str): The name for this property.
            value (str): The value for this property.
            columns (int): The amount of columns to span.
            rows (int): The amount of rows to span.
        """
        super().__init__(name, value)
        self.columns = columns
        self.rows = rows

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{" + self.name + "#}"})

    @property
    def as_dict(self) -> Dict:
        return {
            self.name: self.value,
            self.name + "_row_span": self.rows,
            self.name + "_col_span": self.columns,
        }


class Formula(Property):
    def __init__(self, name: str, formula: str):
        """
        Args:
            name (str): The name for this property.
            formula (str): The formula.
        """
        super().__init__(name, formula)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{>" + self.name + "}"})


class StyledProperty(Property):
    def __init__(
        self,
        name: str,
        value: str,
        font: str = None,
        font_size: Union[str, int] = None,
        font_color: str = None,
        bold: bool = None,
        italic: bool = None,
        underline: bool = None,
        strikethrough: bool = None,
        highlight_color: str = None,
    ):
        """
        Args:
            name (str): The name for this property.
            value (str): The value for this property.
            font (str, optional): The font. Defaults to None.
            font_size (Union[str, int], optional): The font size. Defaults to None.
            font_color (str, optional): The font color. Defaults to None.
            bold (bool, optional): Whether or not the text should be bold. Defaults to None.
            italic (bool, optional): Whether or not the text should be italic. Defaults to None.
            underline (bool, optional): Whether or not the text should be underlined. Defaults to None.
            strikethrough (bool, optional): Whether or not the text should be struckthrough. Defaults to None.
            highlight_color (str, optional): The color in which the text should be highlighted. Defaults to None.
        """
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
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{style " + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        result = {self.name: self.value}

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
    def __init__(
        self,
        name: str,
        text: str,
        color: str = None,
        font: str = None,
        width: Union[int, str] = None,
        height: Union[int, str] = None,
        opacity: float = None,
        rotation: int = None,
    ):
        """
        Args:
            name (str): The name for this property.
            text (str): The text for the watermark.
            color (str, optional): The color for the watermark. Defaults to None.
            font (str, optional): The font for the watermark. Defaults to None.
            width (Union[int, str], optional): The width of the watermark. Defaults to None.
            height (Union[int, str], optional): The height of the watermark. Defaults to None.
            opacity (float, optional): The opacity of the watermark. Defaults to None.
            rotation (int, optional): The rotation of the watermark. Defaults to None.
        """
        super().__init__(name, text)
        self.color: str = color
        self.font: str = font
        self.width: Union[int, str] = width
        self.height: Union[int, str] = height
        self.opacity: float = opacity
        self.rotation: int = rotation

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{watermark " + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        result = {self.name: self.value}

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
    def __init__(self, name: str, code: str, data: Any = None):
        """
        Args:
            name (str): The name for this element.
            code (str): The JSON-encoded code for generating a D3 image.
            data (Any, optional): The data that the code will have access to. Defaults to None.
        """
        super().__init__(name)
        self.code: str = code
        self.data: Any = data

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$d3 " + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        result = {self.name: self.code}

        if self.data is not None:
            result[self.name + "_data"] = self.data

        return result


class COPChartDateOptions:
    """Date options for an COPChart (different from ChartDateOptions in charts.py)."""

    def __init__(
        self, format: str = None, unit: str = None, step: Union[int, str] = None
    ):
        """
        Args:
            format (str, optional): The format to display the date on the chart's axis. Defaults to None.
            unit (str, optional): The unit to be used for spacing the axis values. Defaults to None.
            step (Union[int, str], optional): How many of the above unit should be used for spacing the axis values (automatic if undefined).
                This option is not supported in LibreOffice. Defaults to None.
        """
        self.format: str = format
        self.unit: str = unit
        self.step: Union[int, str] = step

    @property
    def as_dict(self) -> Dict:
        result = {}

        if self.format is not None:
            result["format"] = self.format
        if self.unit is not None:
            result["unit"] = self.unit
        if self.step is not None:
            result["step"] = self.step

        return result


class COPChart(Element):
    """The class for an COPChart. This is used for chart templating."""

    def __init__(
        self,
        name: str,
        x_data: Iterable[Union[str, int, float, Mapping]],
        y_datas: Union[
            Iterable[Iterable[Union[str, int, float, Mapping]]],
            Mapping[str, Iterable[Union[str, int, float, Mapping]]],
        ],
        date: COPChartDateOptions = None,
        title: str = None,
        x_title: str = None,
        y_title: str = None,
        y2_title: str = None,
        x2_title: str = None,
    ):
        """
        Args:
            name (str): The name for this element.
            x_data (Iterable[Union[str, int, float, Mapping]]): The data for the x-axis. Format : ["day 1", "day 2", "day 3", "day 4", "day 5"] or
                [{"value": "day 1"}, {"value": "day 2"}, {"value": "day 3"}, {"value": "day 4"}, {"value": "day 5"}]
            y_datas (Union[Iterable[Iterable[Union[str, int, float, Mapping]]], Mapping[str, Iterable[Union[str, int, float, Mapping]]]]):
                The data for the y-axis in the same format as x_data.
            date (COPChartDateOptions, optional): The date options for the chart. Defaults to None.
            title (str, optional): The title of the chart. Defaults to None.
            x_title (str, optional): The title for the x-axis. Defaults to None.
            y_title (str, optional): The title for the y-axis. Defaults to None.
            y2_title (str, optional): The title for the second y-axis. Defaults to None.
            x2_title (str, optional): The title for the second x-axis. Defaults to None.

        Raises:
            TypeError: raise error when the input data for the y-axis is not valid
        """
        super().__init__(name)
        self.x_data: List = list(x_data)

        self.y_datas: Dict[str, Iterable[Union[str, int, float]]] = None
        """If the argument 'y_datas' is of type Iterable[Iterable], then default names (e.g. series 1, series 2, ...) will be used."""
        if isinstance(y_datas, Mapping):
            self.y_datas = {name: list(data) for name, data in y_datas.items()}
        elif isinstance(y_datas, Iterable):
            self.y_datas = {
                f"series {i+1}": list(data) for i, data in enumerate(y_datas)
            }
        else:
            raise TypeError(
                f'Expected Mapping or Iterable for y_data, got "{type(y_datas)}"'
            )

        self.date: COPChartDateOptions = date
        self.title: str = title
        self.x_title: str = x_title
        self.y_title: str = y_title
        self.x2_title: str = x2_title
        self.y2_title: str = y2_title

    @classmethod
    def from_dataframe(
        cls,
        name: str,
        data: "pandas.DataFrame",
        date: COPChartDateOptions = None,
        title: str = None,
        x_title: str = None,
        y_title: str = None,
        y2_title: str = None,
        x2_title: str = None,
    ) -> "COPChart":
        """Construct an COPChart object from a [Pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

        Args:
            name (str): The name for this element.
            data (pandas.DataFrame): The data for this COPChart in a Pandas dataframe
            date (COPChartDateOptions, optional): The date options for the chart. Defaults to None.
            title (str, optional): The title for the chart. Defaults to None.
            x_title (str, optional): The title for the x-axis. Defaults to None.
            y_title (str, optional): The title for the y-axis. Defaults to None.
            y2_title (str, optional): The title for the second y-axis. Defaults to None.
            x2_title (str, optional): The title for the second x-axis. Defaults to None.

        Returns:
            COPChart: the COPChart object generated from the dataframe
        """
        x_data = list(data.iloc[:, 0])

        y_frame = data.iloc[:, 1:]
        y_datas = {}
        for col_name, col_data in y_frame.iteritems():
            y_datas[col_name] = col_data

        return cls(
            name, x_data, y_datas, date, title, x_title, y_title, y2_title, x2_title
        )

    @property
    def as_dict(self) -> Dict:
        result = {
            "xAxis": {
                "data": self.x_data,
            },
            "yAxis": {
                "series": [
                    {"name": name, "data": data} for name, data in self.y_datas.items()
                ]
            },
        }

        if self.title is not None:
            result["title"] = self.title
        if self.date is not None:
            result["xAxis"]["date"] = self.date.as_dict
        if self.x_title is not None:
            result["xAxis"]["title"] = self.x_title
        if self.y_title is not None:
            result["yAxis"]["title"] = self.y_title
        if self.x2_title is not None:
            result["x2Axis"] = {}
            result["x2Axis"]["title"] = self.x2_title
        if self.y2_title is not None:
            result["y2Axis"] = {}
            result["y2Axis"]["title"] = self.y2_title

        return {self.name: result}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{aopchart " + self.name + "}"})


class PageBreak(Property):
    """The class for a page break property."""

    def __init__(self, name: str, value: Union[str, bool]):
        """
        Args:
            name (str): The name for this property.
            value (Union[str, bool]): Value should be set to 'page' or 'pagebreak' for PageBreak, 'column' or 'columnbreak' for column breaks.
                If set to True (default) it will create a pagebreak.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?" + self.name + "}"})


class MarkdownContent(Property):
    """The class for markdown content."""

    def __init__(self, name: str, value: str):
        """
        Args:
            name (str): The name for this property.
            value (str): Holds the Markdown content.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{_" + self.name + "_}"})


class TextBox(Element):
    """This tag will allow you to insert a text box starting in the cell containing the tag in Excel."""

    def __init__(
        self,
        name: str,
        value: str,
        font: str = None,
        font_color: str = None,
        font_size: Union[int, str] = None,
        transparency: Union[int, str] = None,
        width: Union[int, str] = None,
        height: Union[int, str] = None,
    ):
        """
        Args:
            name (str): The name for this element.
            value (str): The value for this element.
            font (str, optional): The font. Defaults to None.
            font_color (str, optional): The font color. Defaults to None.
            font_size (Union[int, str], optional): The font size. Defaults to None.
            transparency (Union[int, str], optional): The transparency. Defaults to None.
            width (Union[int, str], optional): The width of the text box. Defaults to None.
            height (Union[int, str], optional): The height of the text box. Defaults to None.
        """
        super().__init__(name)
        self.value: str = value
        self.font: str = font
        self.font_color: str = font_color
        self.font_size: Union[int, str] = font_size
        self.transparency: Union[int, str] = transparency
        self.width: Union[int, str] = width
        self.height: Union[int, str] = height

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{tbox " + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        result = {self.name: self.value}

        if self.font is not None:
            result[self.name + "_font"] = self.font
        if self.font_color is not None:
            result[self.name + "_font_color"] = self.font_color
        if self.font_size is not None:
            result[self.name + "_font_size"] = self.font_size
        if self.transparency is not None:
            result[self.name + "_transparency"] = self.transparency
        if self.width is not None:
            result[self.name + "_width"] = self.width
        if self.height is not None:
            result[self.name + "_height"] = self.height

        return result


class Freeze(Property):
    """Only supported in Excel. Represents an object that indicates to put a freeze pane in the excel template."""

    def __init__(self, name: str, value: Union[str, bool]):
        """
        Args:
            name (str): The name for the freeze property.
            value (Union[str, bool]): Three options are avaliable.
             First option, place the pane where the tag is located, using a value of **true**.
             Second option, provide the location to place the pane, e.g. **"C5"**, in the format of excel cell and row.
             Third option, don't place a pane, using a value of **false**.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{freeze " + self.name + "}"})


class Insert(Property):
    """Inside Word and PowerPoint and Excel documents, the tag {?insert fileToInsert} can be used to insert files like Word, Excel, Powerpoint and PDF documents.
    Please use `ExcelInsert` element to insert in excel with more flexibility.
    """

    def __init__(self, name: str, value: str):
        """
        Args:
            name (str): The name for the insert tag.
            value (str): Base64 encoded document that needs to be inserted in output docx or pptx.
            The document can be docx, pptx, xlsx, or pdf documents.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?insert " + self.name + "}"})
    
class PdfInclude(Element):
    """Inside Word and PowerPoint and Excel documents, the tag {?include pdf } can be used to include files like Word, Excel, Powerpoint and PDF documents.
    Please use `ExcelInsert` element to insert in excel with more flexibility.
    """
    def __init__(self, name: str , value: str, filename: str, mime_type: str, file_content: str, file_source: str):
        """
        Args:
            name (str): The tag name referenced in templates
            filename (str): Name of the file to include
            mime_type (str): MIME type of the content (e.g., 'image/png')
            file_content (str): Base64 encoded content of the file
            file_source (str): Source type ('base64', 'local', etc.)
        """
        super().__init__(name)
        self.value = value
        self.filename = filename
        self.mime_type = mime_type
        self.file_content = file_content
        self.file_source = file_source

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?pdfinclude " + self.name + "}"})
    

    @property
    def as_dict(self) -> Dict:
        result = {}
        result [self.name] = {}

        if self.filename is not None:
            result [self.name]["name"] = self.filename
        if self.mime_type is not None:
            result [self.name]["mime_type"] = self.mime_type
        if self.file_content is not None:
            result [self.name]["file_content"] = self.file_content
        if self.file_source is not None:
            result [self.name]["file_source"] = self.file_source

        return result
        

class PptxShapeRemove(Property):
    """Allows the removal of an entire shape / text-box if the associated tag evaluates to false. For example, if a template slide includes a text box with the tag {toShow?} and 
    the value of toShow is false or undefined, the entire shape will be removed from the slide.
    """
    def __init__(self, name: str, value:  Union[bool, str]):
        """
        Args:
            name (str): The name for the remove tag.
            value (bool or string): False (to remove the shape / text-box) or string/True
            The document should be, pptx.
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{ " + self.name + "?" + "}"})
    

class HideSlide(Property):
    """Allows hiding a slide.
    LIMITATION: using _hide for slide hide is that it can only be used for hiding slides during generation(!slideGeneration)
    """
    def __init__(self, name: str, condition : str ):
        """
        Args:
            name (str): Name/identifier for this hide condition
            condition (str): The condition to determine when to hide the slide
            The document should be, pptx.
        """
        super().__init__(name, condition)
    
    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{hide " + self.name + "}"})
      
class HideSheets(Property):
    """Allows hiding a sheet in Excel documents. 
    Can be used to hide sheets based on conditions during generation.
    The hide tag {hide condition} is replaced by nothing but will hide the sheet if the condition evaluates to true.
    The condition can use any Angular expressions that are supported.

    """

    def __init__(self, name: str, condition: str):
        """
        Args:
            name (str): Name/identifier for this hide condition 
            condition (str): Angular expression that determines when to hide the sheet.
                The document must be an Excel workbook (.xlsx)
        """
        super().__init__(name, condition)
    
    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{hide " + self.name + "}"})
    
    
class ExcelInsert(Element):
    """Inside Excel it is posiible to insert word, powerpoint, excel and pdf file using AOP tag {?insert fileToInsert}.
        Options available are:  you can provide dynamic icon and icon position.
    """

    def __init__(self,
                 name: str,
                 value: str,
                 #  isPreview: bool = None,
                 icon: str = None,
                 fromRow: int = None,
                 fromCol: Union[str, int] = None,
                 fromRowOff: str = None,
                 fromColOff: str = None,
                 toRow: int = None,
                 toCol: Union[str, int] = None,
                 toRowOff: str = None,
                 toColOff: str = None
                 ):
        """It is possible to provide dynamic icon and position of icon.

        Args:
            name (str):  Name of insert tag. Ex(fileToInsert)
            value (str): File to insert of path to file. (Source can be FTP, SFTP, URL or base64encoded file.)
            icon (str, optional): Icon that links the file to insert. Once clicked on it, opens the file inserted. If it is not provide default icon is used.
            fromRow (int, optional): position for top of icon. Defaults to row of the tag.
            fromCol (Union[str,int], optional): positon for left of icon. Defaults to column of the tag.
            fromRowOff (str, optional): space after the value of from Row. Defaults to 0.
            fromColOff (str, optional): space after the value of fromCol. Defaults to 0.
            toRow (int, optional): position for bottom of icon. Defaults to row of the tag + 3.
            toCol (Union[str,int], optional): position for right side of icon. Defaults to column of the tag.
            toRowOff (str, optional): space after toRow value. Defaults to 20px.
            toColOff (str, optional): space after toCol value. Defaults to 50px.
        """
        super().__init__(name)
        self.value: str = value
        # self.isPreview: bool = isPreview
        self.icon: str = icon
        self.fromRow: int = fromRow
        self.fromCol: Union[str, int] = fromCol
        self.fromRowOff: str = fromRowOff
        self.fromColOff: str = fromColOff
        self.toRow: int = toRow
        self.toCol: Union[str, int] = toCol
        self.toRowOff: str = toRowOff
        self.toColOff: str = toColOff

    @property
    def as_dict(self) -> Dict:
        result = {
            self.name: self.value
        }
        # if self.isPreview is not None:
        #     result[self.name+'_isPreview'] = self.isPreview
        if self.icon is not None:
            result[self.name+'_icon'] = self.icon
        if self.fromRow is not None:
            result[self.name+'_fromRow'] = self.fromRow
        if self.fromCol is not None:
            result[self.name+'_fromCol'] = self.fromCol
        if self.fromRowOff is not None:
            result[self.name+'_fromRowOff'] = self.fromRowOff
        if self.fromColOff is not None:
            result[self.name+'_fromColOff'] = self.fromColOff
        if self.toRow is not None:
            result[self.name+'_toRow'] = self.toRow
        if self.toCol is not None:
            result[self.name+'_toCol'] = self.toCol
        if self.toRowOff is not None:
            result[self.name+'_toRowOff'] = self.toRowOff
        if self.toColOff is not None:
            result[self.name+'_toColOff'] = self.toColOff

        return result

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?insert fileToInsert}"})


class Embed(Property):
    """Inside Word, it is possible to copy the content of one docx file to the template without rendering.

        To do so, you can use AOP embed tag as {?embed fileToEmbed} where fileToEmbed contains the path of file or file itself.

        The content of fileToEmbed replaces the tag

        Only supported in Word and only supports docx file to embed.
    """

    def __init__(self, name: str, value: str):
        """It takes the tagName and its value as parameter.

        Args:
            name (str): Name of the tag (ex. fileToEmbed)
            value (str): File to embed. Source can be FTP, SFTP, URL or base64 encoded file. (ex. base64encoded string)
        """
        super().__init__(name, value)

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{?embed fileToEmbed}"})


class SheetProtection(Element):
    """Inside Excel documents, this tag can be used to make password protected sheets. This tag has the feature of password along with different other features.

        Note: value is considered password, so try to use only one (either value or passowrd).
    """

    def __init__(self,
                 name: str,
                 value: str = None,
                 autoFilter: str = None,
                 deleteColumns: bool = None,
                 deleteRows: bool = None,
                 formatCells: bool = None,
                 formatColumns: bool = None,
                 formatRows: bool = None,
                 insertColumns: bool = None,
                 insertHyperlinks: bool = None,
                 insertRows: bool = None,
                 password: str = None,
                 pivotTables: bool = None,
                 selectLockedCells: bool = None,
                 selectUnlockedCells: bool = None,
                 sort: bool = None,
                 ):
        """
        Args:
            name (str): The name for the sheet protection tag.
            value (str): Value for the tag; this is used as password
            autoFilter (str): lock auto filter in sheet.
            deleteColumns (bool): lock delete columns in sheet.
            deleteRows (bool): lock delete rows in sheet.
            formatCells (bool): lock format cells.
            formatColumns (bool): lock format columns.
            formatRows (bool): lock format rows.
            insertColumns (bool): lock insert columns.
            insertHyperlinks (bool): lock insert hyperlinks.
            insertRows (bool): lock insert rows.
            password (str): password to lock with.
            pivotTables (bool): lock pivot tables.
            selectLockedCells (bool): lock select locked cells.
            selectUnlockedCells (bool): lock select unlocked cells.
            sort (bool): lock sort.
        """
        super().__init__(name)
        self.value = value
        self.autoFilter = autoFilter
        self.deleteColumns = deleteColumns
        self.deleteRows = deleteRows
        self.formatCells = formatCells
        self.formatColumns = formatColumns
        self.formatRows = formatRows
        self.insertColumns = insertColumns
        self.insertHyperlinks = insertHyperlinks
        self.insertRows = insertRows
        self.password = password
        self.pivotTables = pivotTables
        self.selectLockedCells = selectLockedCells
        self.selectUnlockedCells = selectUnlockedCells
        self.sort = sort

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{protect " + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        result = {}
        if self.value is not None:
            result[self.name] = self.value
        if self.autoFilter is not None:
            result[self.name+'_allow_auto_filter'] = self.autoFilter
        if self.deleteColumns is not None:
            result[self.name+'_allow_delete_columns'] = self.deleteColumns
        if self.deleteRows is not None:
            result[self.name+'_allow_delete_rows'] = self.deleteRows
        if self.formatCells is not None:
            result[self.name+'_allow_format_cells'] = self.formatCells
        if self.formatColumns is not None:
            result[self.name+'_allow_format_columns'] = self.formatColumns
        if self.formatRows is not None:
            result[self.name+'_allow_format_rows'] = self.formatRows
        if self.insertColumns is not None:
            result[self.name+'_allow_insert_columns'] = self.insertColumns
        if self.insertHyperlinks is not None:
            result[self.name+'_allow_insert_hyperlinks'] = self.insertHyperlinks
        if self.insertRows is not None:
            result[self.name+'_allow_insert_rows'] = self.insertRows
        if self.password is not None:
            result[self.name+'_password'] = self.password
        if self.pivotTables is not None:
            result[self.name+'_allow_pivot_tables'] = self.pivotTables
        if self.selectLockedCells is not None:
            result[self.name+'_allow_select_locked_cells'] = self.selectLockedCells
        if self.selectUnlockedCells is not None:
            result[self.name+'_allow_select_unlocked_cells'] = self.selectUnlockedCells
        if self.sort is not None:
            result[self.name+'_allow_sort'] = self.sort
        return result


class ValidateCell(Element):
    """
    It is possible to insert cell validation in excel using validate tag as {validate validateTag} (validate keyword followed by tagName)
    """

    def __init__(self,
                 name: str,
                 ignoreBlank: bool = None,
                 allow: str = None,
                 value1: str = None,
                 value2: str = None,
                 inCellDropdown: bool = None,
                 data: str = None,
                 showInputMessage: bool = None,
                 inputTitle: str = None,
                 inputMessage: str = None,
                 showErrorAlert: bool = None,
                 errorStyle: str = None,
                 errorTitle: str = None,
                 errorMessage: str = None,
                 ):
        """Available option while using validate cell are ( ignoreBlank, allow, value1, value2, inCellDropdown, data, showInputMessage, inputTitle, inputMessage, showErrorAlert, errorStyle, errorTitle,errorMessage )

        Args:
            name (string, optional): Name of the validate tag. For {validate tagName}, tagName is name for this element. 
            ignoreBlank (bool, optional): Set it to false for not allowing empty values in cell. The value is true by default.
            allow (string, optional): Type of data used for validation. Available options are (anyValue, whole, decimal, list, date, time, textLength, custom). Please use camelCase to insert value for allow attribute.
            value1 (string, optional): Value to compare with.
            value2 (string, optional): Value to compare with.<br>
            <i>Note:
                These two options <strong>(_value1, _value2)</strong> can be used for any allow/type of validation that require values for comparison, in such case use <strong>"_value1"</strong> attribute as the first value to be passed and <strong>"_value2"</strong> attribute as the 2nd value.<br><br>
                Some allow type of validation require only one value to compare; in such case use <strong>"_value1"</strong> attribute.<br><br>
                For ex :<br>
                If allow type of validation is date and you have to check in between two dates.<br>
                Then you could use <strong>"_value1"</strong> attribute as start date and <strong>"_value2"</strong> attribute as end date.<br><br>
                If allow type of validation is whole and you have to check for value less than 100.<br>
                Then you could use <strong>"_value1"</strong> for that value and do not use "<strong>_value2".</strong><br><br>
                While using time and date as allow type validation, please provide date/time with correct formatting.<br>
                for time: <strong>hours:minutes:seconds</strong> i.e hours , minutes, seconds separated by colon (:)<br>
                    ex : 14:30:00 for 2:30 pm<br><br>
                for date: <strong>month/day/year</strong> i.e day, month , year separated by forward slash(/)<br>
                    ex : 02/07/2023 for Feb 7 2023.<br><br>
                for list: you could use normal string with elements separated by comma(,).<br>
                    ex : "first, second, third" for list of three elements.<br></i>
            inCellDropdown (bool, optional): Set it to false for not showing dropdown button while validation allow type is list. It is true by default for list allow type.
            data (string, optional): Type of comparison to be done for the cell value. Available values are (lessThanOrEqual, notBetween, equal, notEqual, greaterThan, greaterThan, lessThan, greaterThanOrEqual, lessThanOrEqual). Default value is "between". Please use camelCase for the value as shown in examples.
            showInputMessage (bool, optional): Set it to false to hide message shown when the cell to validate is being selected. The value for it is true by default.
            inputTitle (string, optional): Title of message to be shown when cell to validate is selected.
            inputMessage (string, optional): Message to be shown when cell to validate is selected.
            showErrorAlert (bool, optional): Set it to false, if you want to hide error alert once cell validation fails. The value is true by default.
            errorStyle (string, optional): Type of error style when cell validation fails. The value is stop by default. Available options are(stop,waring, Information).
            errorTitle (string, optional): Title of error to be shown when cell validation fails.
            errorMessage (string, optional): Message of error to be shown when cell validation fails.
        """
        super().__init__(name)
        self.ignoreBlank = ignoreBlank
        self.allow = allow
        self.value1 = value1
        self.value2 = value2
        self.inCellDropdown = inCellDropdown
        self.data = data
        self.showInputMessage = showInputMessage
        self.inputTitle = inputTitle
        self.inputMessage = inputMessage
        self.showErrorAlert = showErrorAlert
        self.errorStyle = errorStyle
        self.errorTitle = errorTitle
        self.errorMessage = errorMessage

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{validate " + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        result = {}
        if self.ignoreBlank is not None:
            result[self.name + '_ignore_blank'] = self.ignoreBlank
        if self.allow is not None:
            result[self.name + '_allow'] = self.allow
        if self.value1 is not None:
            result[self.name + '_value1'] = self.value1
        if self.value2 is not None:
            result[self.name + '_value2'] = self.value2
        if self.inCellDropdown is not None:
            result[self.name + '_in_cell_dropdown'] = self.inCellDropdown
        if self.data is not None:
            result[self.name + '_data'] = self.data
        if self.showInputMessage is not None:
            result[self.name + '_show_input_message'] = self.showInputMessage
        if self.inputTitle is not None:
            result[self.name + '_input_title'] = self.inputTitle
        if self.inputMessage is not None:
            result[self.name + '_input_message'] = self.inputMessage
        if self.showErrorAlert is not None:
            result[self.name + '_show_error_alert'] = self.showErrorAlert
        if self.errorStyle is not None:
            result[self.name + '_error_style'] = self.errorStyle
        if self.errorTitle is not None:
            result[self.name + '_error_title'] = self.errorTitle
        if self.errorMessage is not None:
            result[self.name + '_error_message'] = self.errorMessage
        return result


class Link(Property):
    """The class for the link/target tags.
    This tags allows you to place a link to a target in the same document.
    If the uid is not provided, a new uid will be generated uniquely for every link and target pair.
    """

    def __init__(
        self,
        name: str,
        value: str,
        uid_name: str = None,
        uid_value: str = None,
    ):
        """Create a new link/target tag pair.
        If the uid is not provided, a new uid will be generated uniquely for each link/target pair.

        Args:
            name (str): the name of the link/target tags.
            value (str): the value of the link/target tags.
            uid_name (str): the name of the uid of the link/target pair.
            uid_value (str): the value of the uid of the link/target pair.
        """
        super().__init__(name, value)
        self.uid_name = uid_name
        self.uid_value = uid_value

    @property
    def available_tags(self) -> FrozenSet[str]:
        if self.uid_name and self.uid_value:
            return frozenset(
                {
                    "{link" + self.name + ":" + self.uid_name + "}",
                    "{target" + self.name + ":" + self.uid_name + "}",
                }
            )
        return frozenset({"{link" + self.name + "}", "{target" + self.name + "}"})

    @property
    def as_dict(self) -> Dict:
        if self.uid_name and self.uid_value:
            return {self.name: self.value, self.uid_name: self.uid_value}
        return {self.name: self.value}


class ElementCollection(list, Element):
    """A collection used to group multiple elements together.
    It can contain nested `ElementCollection`s and should be used to pass multiple `Element`s as PrintJob data, as well as to allow for nested elements.
    Its name is used as a key name when nested, but ignored for all purposes when it's the outer ElementCollection.
    """

    def __init__(self, name: str = "", elements: Iterable[Element] = ()):
        """
        Args:
            name (str, optional): The name for this element collection. Not used for the outer ElementCollection, but needed for nested ElementCollections Defaults to "".
            elements (Iterable[Element], optional): An iterable containing the elements that need to be added to this collection. Defaults to ().
        """
        list.__init__(self, elements)
        Element.__init__(self, name)

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation for this object.
        """
        return self.json

    def __repr__(self) -> str:
        """
        Returns:
            str: The JSON representation for this object.
        """
        return self.json

    def copy(self) -> "ElementCollection":
        """
        Returns:
            ElementCollection: A copy of this element collection.
        """
        return self.__class__(self)

    def deepcopy(self) -> "ElementCollection":
        """
        Returns:
            ElementCollection: A deep copy of this element collection.
        """
        return deepcopy(self)

    @property
    def json(self):
        return json.dumps(self.as_dict)

    def add(self, element: Element):
        """Add an element to this element collection object.

        Args:
            element (Element): the element to add to this collection
        """
        self.append(element)

    def add_all(self, obj: "ElementCollection"):
        """Add all the elements in the given collection to this collection.

        Args:
            obj (ElementCollection): the collection of which the elements need to be added to this element collection object
        """
        for element in obj:
            self.add(element)

    def remove_element_by_name(self, element_name: str):
        """Remove an element from this element collection object by its name.

        Args:
            element_name (str): the name of the element that needs to be removed
        """
        self.remove(
            next(element for element in self if element.name == element_name))

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
    def element_to_element_collection(
        cls, element: Element, name: str = ""
    ) -> "ElementCollection":
        """Generate an element collection from an element and a name.

        Args:
            element (Element): the element that needs to be transformed to an element collection
            name (str): The name of the element collection. Defaults to ''.

        Returns:
            ElementCollection: the generated element collection from an element and a name
        """
        return cls.from_mapping(element.as_dict, name)

    @classmethod
    def from_mapping(cls, mapping: Mapping, name: str = "") -> "ElementCollection":
        """Generate an element collection from a mapping and a name.

        Args:
            mapping (Mapping): the mapping that needs to be converted to an element collection
            name (str): The name of the element collection. Defaults to ''.

        Returns:
            ElementCollection: an element collection generated from the given mapping and name
        """
        result_set = set()
        for key, value in mapping.items():
            result_set.add(Property(key, value))
        return cls(name, result_set)

    @classmethod
    def from_json(cls, json_str: str, name: str = "") -> "ElementCollection":
        """Generate an element collection from a JSON string.

        Args:
            json_str (str): the json string that needs to be transformed to an element collection
            name (str): The name of the element collection. Defaults to ''.

        Returns:
            ElementCollection: an element collection generated from the given JSON string and name
        """
        return cls.from_mapping(json.loads(json_str), name)
