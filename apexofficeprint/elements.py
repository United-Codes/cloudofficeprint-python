"""
Elements are used to replace the various tags in a template with actual data.
"""

import json
from copy import deepcopy
from typing import Union, List, Iterable, Mapping, Set, FrozenSet
from abc import abstractmethod, ABC
from collections.abc import MutableSet


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
    pass  # TODO


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
ForEachSheet = ForEachSlide
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
        self.max_width = max_width
        """ """
        self.max_height = max_height
        """ """
        self.alt_text = alt_text
        self.wrap_text = wrap_text
        self.rotation = rotation

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
        self.url = url

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
        self._base64 = base64str

    @property
    def base64(self) -> str:
        return self._base64

    @base64.setter
    def base64(self, value: str):
        self._base64 = value

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


class Object(list, Element):
    """# TODO
    """

    def __init__(self, elements: Iterable[Element] = []):
        super().__init__(elements)

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

    @property
    def as_list(self) -> List[dict]:
        """Compile the dict representations of these elements as a `List[dict]`.

        Returns:
            List[dict]: list of elements in this object
        """
        return [element.as_dict for element in self]

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
    def from_mapping(cls, mapping: Mapping) -> 'Object':
        result_set = set()
        for key, value in mapping.items():
            result_set.add(Property(key, value))
        return cls(result_set)

    @classmethod
    def from_json(cls, json_str: str) -> 'Object':
        return cls.from_mapping(json.loads(json_str))
