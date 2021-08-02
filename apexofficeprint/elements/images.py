from typing import Dict, FrozenSet, Union
from ..own_utils import file_utils
from .elements import Element

class Image(Element):
    """The class for image elements."""

    def __init__(self,
                 name: str,
                 source: str,
                 max_width: Union[int, str]=None,
                 max_height: Union[int, str]=None,
                 alt_text: str=None,
                 wrap_text: str=None,
                 rotation: int=None,
                 transparency: Union[int, str]=None,
                 url: str=None,
                 width: Union[int, str]=None,
                 height: Union[int, str]=None):
        """
        Args:
            name (str): The name of the image element.
            source (str): The source for the image: base64 or URL.
            max_width (Union[int, str]): The maximum width of the image (for proportional scaling).
            max_height (Union[int, str]): The maximum height of the image (for proportional scaling).
            alt_text (str): The alternative text for the image, used when the image can't be loaded.
            wrap_text (str): The wrapping mode of the text around the image. The options are:
                In line with text: This option is the default. If no wrap option specified images will wrapped in line with text;
                Square : In order to use this property, wrap option should be "square";
                Top and Bottom : In order to use this property, wrap option should be "top-bottom";
                Behind Text : In order to use this property, wrap option should be "behind";
                In Front of Text : In order to use this property, wrap option should be "front".
            rotation (int): The rotation of the image in degrees.
            transparency (Union[int, str]): The transparency of the image in percent.
            url (str): The URL to load when the image is clicked.
            width (Union[int, str]): The width of the image (for non-proportional scaling).
            height (Union[int, str]): The height of the image (for non-proportional scaling).
        """
        super().__init__(name)
        self.source: str = source
        self.max_width: Union[int, str] = max_width
        self.max_height: Union[int, str] = max_height
        self.alt_text: str = alt_text
        self.wrap_text: str = wrap_text
        self.rotation: int = rotation
        self.transparency: Union[int, str] = transparency
        self.url: str = url
        self.width: Union[int, str] = width
        self.height: Union[int, str] = height

    @property
    def alt_text(self) -> str:
        """Getter for alt_text

        Returns:
            str: alternative text
        """
        return self._alt_text

    @alt_text.setter
    def alt_text(self, value: str):
        """Setter for alt_text

        Args:
            value (str): new value for alt_text
        """
        self._alt_text = None if value == "" else value

    @property
    def wrap_text(self) -> str:
        """Getter for wrap_text

        Returns:
            str: the wrapping mode of the text around the image
        """
        return self._wrap_text if self._wrap_text else "inline"

    @wrap_text.setter
    def wrap_text(self, value: str):
        """Setter for wrap_text

        Args:
            value (str): new value for wrap_text
        """
        self._wrap_text = None if value == "inline" else value

    @property
    def rotation(self) -> int:
        """Getter for rotation

        Returns:
            int: The image rotation in degrees
        """
        return self._rotation if self._rotation else 0

    @rotation.setter
    def rotation(self, value: int):
        """Setter for rotation

        Args:
            value (int): new value for rotation
        """
        self._rotation = None if value == 0 else value

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{%" + self.name + "}"})

    @property
    def _dict_suffixes(self) -> Dict:
        """The suffixes that need to be appended to this element's name in the dict representation of this Image object.

        Returns:
            Dict: the suffixes that need to be appended to this element's name in the dict representation of this Image object
        """
        result = {}

        if self.max_width is not None:
            result["_max_width"] = self.max_width
        if self.max_height is not None:
            result["_max_height"] = self.max_height
        if self._alt_text is not None:
            result["_alt_text"] = self._alt_text
        if self._wrap_text is not None:
            result["_wrap_text"] = self._wrap_text
        if self._rotation is not None:
            result["_rotation"] = self._rotation
        if self.transparency is not None:
            result["_transparency"] = self.transparency
        if self.url is not None:
            result["_url"] = self.url
        if self.width is not None:
            result["_width"] = self.width
        if self.height is not None:
            result["_height"] = self.height

        return result

    @property
    def as_dict(self) -> Dict:
        result = {
            self.name: self.source,
        }

        for suffix, value in self._dict_suffixes.items():
            result[self.name + suffix] = value
        return result

    @staticmethod
    def from_file(
            name: str,
            path: str,
            max_width: Union[int, str]=None,
            max_height: Union[int, str]=None,
            alt_text: str=None,
            wrap_text: str=None,
            rotation: int=None,
            transparency: Union[int, str]=None,
            url: str=None,
            width: Union[int, str]=None,
            height: Union[int, str]=None
        ) -> 'Image':
        """Generate an Image object from a local file.

        Args:
            name (str): The name of the image element.
            path (str): The path to the local image.
            max_width (Union[int, str]): The maximum width of the image (for proportional scaling).
            max_height (Union[int, str]): The maximum height of the image (for proportional scaling).
            alt_text (str): The alternative text for the image, used when the image can't be loaded.
            wrap_text (str): The wrapping mode of the text around the image. The options are:
                In line with text: This option is the default. If no wrap option specified images will wrapped in line with text;
                Square : In order to use this property, wrap option should be "square";
                Top and Bottom : In order to use this property, wrap option should be "top-bottom";
                Behind Text : In order to use this property, wrap option should be "behind";
                In Front of Text : In order to use this property, wrap option should be "front".
            rotation (int): The rotation of the image in degrees.
            transparency (Union[int, str]): The transparency of the image in percent.
            url (str): The URL to load when the image is clicked.
            width (Union[int, str]): The width of the image (for non-proportional scaling).
            height (Union[int, str]): The height of the image (for non-proportional scaling).

        Returns:
            Image: the generated Image object from a local file
        """
        return Image(
            name,
            file_utils.read_file_as_base64(path),
            max_width,
            max_height,
            alt_text,
            wrap_text,
            rotation,
            transparency,
            url,
            width,
            height,
        )

    @staticmethod
    def from_raw(
            name: str,
            data: bytes,
            max_width: Union[int, str]=None,
            max_height: Union[int, str]=None,
            alt_text: str=None,
            wrap_text: str=None,
            rotation: int=None,
            transparency: Union[int, str]=None,
            url: str=None,
            width: Union[int, str]=None,
            height: Union[int, str]=None
        ) -> 'Image':
        """Generate an Image object from raw data.

        Args:
            name (str): The name of the image element.
            data (bytes): The raw data for the image.
            max_width (Union[int, str]): The maximum width of the image (for proportional scaling).
            max_height (Union[int, str]): The maximum height of the image (for proportional scaling).
            alt_text (str): The alternative text for the image, used when the image can't be loaded.
            wrap_text (str): The wrapping mode of the text around the image. The options are:
                In line with text: This option is the default. If no wrap option specified images will wrapped in line with text;
                Square : In order to use this property, wrap option should be "square";
                Top and Bottom : In order to use this property, wrap option should be "top-bottom";
                Behind Text : In order to use this property, wrap option should be "behind";
                In Front of Text : In order to use this property, wrap option should be "front".
            rotation (int): The rotation of the image in degrees.
            transparency (Union[int, str]): The transparency of the image in percent.
            url (str): The URL to load when the image is clicked.
            width (Union[int, str]): The width of the image (for non-proportional scaling).
            height (Union[int, str]): The height of the image (for non-proportional scaling).

        Returns:
            Image: the generated Image object from raw data
        """
        return Image(
            name,
            file_utils.raw_to_base64(data),
            max_width,
            max_height,
            alt_text,
            wrap_text,
            rotation,
            transparency,
            url,
            width,
            height,
        )

    @staticmethod
    def from_base64(
            name: str,
            base64str: str,
            max_width: Union[int, str]=None,
            max_height: Union[int, str]=None,
            alt_text: str=None,
            wrap_text: str=None,
            rotation: int=None,
            transparency: Union[int, str]=None,
            url: str=None,
            width: Union[int, str]=None,
            height: Union[int, str]=None
        ) -> 'Image':
        """Generate an Image object from a base64 string.

        Args:
            name (str): The name of the image element.
            base64str (str): The base64 string for the image.
            max_width (Union[int, str]): The maximum width of the image (for proportional scaling).
            max_height (Union[int, str]): The maximum height of the image (for proportional scaling).
            alt_text (str): The alternative text for the image, used when the image can't be loaded.
            wrap_text (str): The wrapping mode of the text around the image. The options are:
                In line with text: This option is the default. If no wrap option specified images will wrapped in line with text;
                Square : In order to use this property, wrap option should be "square";
                Top and Bottom : In order to use this property, wrap option should be "top-bottom";
                Behind Text : In order to use this property, wrap option should be "behind";
                In Front of Text : In order to use this property, wrap option should be "front".
            rotation (int): The rotation of the image in degrees.
            transparency (Union[int, str]): The transparency of the image in percent.
            url (str): The URL to load when the image is clicked.
            width (Union[int, str]): The width of the image (for non-proportional scaling).
            height (Union[int, str]): The height of the image (for non-proportional scaling).

        Returns:
            Image: the generated Image object from a base64 string
        """
        return Image(
            name,
            base64str,
            max_width,
            max_height,
            alt_text,
            wrap_text,
            rotation,
            transparency,
            url,
            width,
            height,
        )

    @staticmethod
    def from_url(
            name: str,
            url_source: str,
            max_width: Union[int, str]=None,
            max_height: Union[int, str]=None,
            alt_text: str=None,
            wrap_text: str=None,
            rotation: int=None,
            transparency: Union[int, str]=None,
            url: str=None,
            width: Union[int, str]=None,
            height: Union[int, str]=None
        ) -> 'Image':
        """Generate an Image object from a URL.

        Args:
            name (str): The name of the image element.
            url (str): The URL for the image.
            max_width (Union[int, str]): The maximum width of the image (for proportional scaling).
            max_height (Union[int, str]): The maximum height of the image (for proportional scaling).
            alt_text (str): The alternative text for the image, used when the image can't be loaded.
            wrap_text (str): The wrapping mode of the text around the image. The options are:
                In line with text: This option is the default. If no wrap option specified images will wrapped in line with text;
                Square : In order to use this property, wrap option should be "square";
                Top and Bottom : In order to use this property, wrap option should be "top-bottom";
                Behind Text : In order to use this property, wrap option should be "behind";
                In Front of Text : In order to use this property, wrap option should be "front".
            rotation (int): The rotation of the image in degrees.
            transparency (Union[int, str]): The transparency of the image in percent.
            url (str): The URL to load when the image is clicked.
            width (Union[int, str]): The width of the image (for non-proportional scaling).
            height (Union[int, str]): The height of the image (for non-proportional scaling).

        Returns:
            Image: the generated Image object from a URL
        """
        return Image(
            name,
            url_source,
            max_width,
            max_height,
            alt_text,
            wrap_text,
            rotation,
            transparency,
            url,
            width,
            height,
        )
