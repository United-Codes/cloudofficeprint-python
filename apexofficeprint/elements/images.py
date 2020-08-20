from abc import ABC, abstractmethod
from typing import FrozenSet
from .._utils import file_utils
from .elements import Element

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
