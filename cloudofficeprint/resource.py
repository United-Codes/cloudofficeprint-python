"""
Module containing the Resource class and its subclasses, which is also exposed at package level.

Every resource contains or points to a file to be used as a template or to be included as an append/prepend document (in case of pdf output).

## Resource creation

`Resource` is the base class which should not be constructed.
The recommended way of obtaining a `Resource` is through the static from_... methods (e.g. `Resource.from_local_file`),
alternatively, the `Resource` subclasses can be constructed to form a valid `Resource`.
"""

import json
from typing import Dict, Union
from abc import abstractmethod, ABC

from .own_utils import type_utils, file_utils


class Resource(ABC):
    """The abstract base class for the resources."""

    def __init__(
        self,
        data: Union[str, bytes] = None,
        filetype: str = None,
    ):
        """Create a new Resource

        Args:
            data (Union[str, bytes], optional): the data for this Resource. Defaults to None.
            filetype (str, optional): the file type of this resource. Defaults to None.
        """
        self.data: Union[str, bytes] = data
        self.filetype: str = filetype

    @property
    def mimetype(self) -> str:
        """
        Returns:
            str: the mime type of the Resource
        """
        return type_utils.extension_to_mimetype(self.filetype)

    @property
    def template_json(self) -> str:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return json.dumps(self.template_dict)

    @property
    @abstractmethod
    def template_dict(self) -> Dict:
        """
        Returns:
            Dict: the dictionary representation of this resource.
        """
        pass

    @property
    def secondary_file_json(self) -> str:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return json.dumps(self.secondary_file_dict)

    @property
    @abstractmethod
    def secondary_file_dict(self) -> Dict:
        """
        Returns:
            Dict: the dictionarty representation of this resource as a secondary file (prepend, append, insert, as subtemplate).
        """
        pass

    def __str__(self) -> str:
        """Override the string representation of this class to return the template-style json.

        Returns:
            str: the JSON representation of this resource as a template.
        """
        return self.template_json

    @staticmethod
    def from_raw(raw_data: bytes, filetype: str) -> "RawResource":
        """Create a RawResource from raw file data..

        Args:
            raw_data (bytes): the raw data as a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object).
            filetype (str): the file type (extension).

        Returns:
            RawResource: the created RawResource.
        """
        return RawResource(raw_data, filetype)

    @staticmethod
    def from_base64(base64string: str, filetype: str) -> "Base64Resource":
        """Create a Base64Resource from a base64 string.

        Args:
            base64string (str): the base64 encoded representation of a file.
            filetype (str): the file type (extension).

        Returns:
            Base64Resource: the created Base64Resource.
        """
        return Base64Resource(base64string, filetype)

    @staticmethod
    def from_local_file(local_path: str) -> "Base64Resource":
        """Create a Base64Resource with the contents of a local file.
        The filetype is determined by the extension of the file.

        Throws IOError if it can't read the file.

        Args:
            local_path (str): the path to local file.

        Returns:
            Base64Resource: the created Base64Resource.
        """
        return Base64Resource(
            file_utils.read_file_as_base64(local_path),
            type_utils.path_to_extension(local_path),
        )

    @staticmethod
    def from_server_path(path: str) -> "ServerPathResource":
        """Create a ServerPathResource targeting a file on the server.
        The filetype is determined by the extension of the file.

        Args:
            path (str): the location of target file on the server.

        Returns:
            ServerPathResource: the created ServerPathResource.
        """
        return ServerPathResource(path)

    @staticmethod
    def from_url(url: str, filetype: str) -> "URLResource":
        """Create an URLResource targeting the file at a given url.

        Args:
            url (str): the file url.
            filetype (str): the file type (extension).

        Returns:
            URLResource: the created URLResource.
        """
        return URLResource(url, filetype)

    @staticmethod
    def from_html(htmlstring: str, landscape: bool = False) -> "HTMLResource":
        """Create an HTMLResource with html data in plain text.
        Landscape is not supported for prepend/append sources, only for template resources.

        Args:
            htmlstring (str): the html content.
            landscape (bool, optional): whether or not to use the landscape option. Defaults to False.

        Returns:
            HTMLResource: the created HTMLResource.
        """
        return HTMLResource(htmlstring, landscape)


class RawResource(Resource):
    """A `Resource` containing raw binary data."""

    def __init__(self, raw_data: bytes, filetype: str):
        """Create a new RawResource.

        Args:
            raw_data (bytes): the raw data as a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object).
            filetype (str): the file type (extension).
        """
        super().__init__(raw_data, filetype)

    @property
    def base64(self) -> str:
        """
        Returns:
            str: the base64 representation of the raw data in `RawResource.data`.
        """
        return file_utils.raw_to_base64(self.data)

    @property
    def template_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "template_type": self.filetype,
            "file": self.base64,
        }

    @property
    def secondary_file_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "mime_type": self.mimetype,
            "file_source": "base64",
            "file_content": self.base64,
        }


class Base64Resource(Resource):
    """A `Resource` containing base64 data."""

    def __init__(
        self,
        base64string: str,
        filetype: str,
    ):
        """Create a new Base64Resource.

        Args:
            base64string (str): the base64 encoded data.
            filetype (str): the file type (extension).
        """
        super().__init__(base64string, filetype)

    @property
    def template_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "template_type": self.filetype,
            "file": self.data,
        }

    @property
    def secondary_file_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "mime_type": self.mimetype,
            "file_source": "base64",
            "file_content": self.data,
        }


class ServerPathResource(Resource):
    """A `Resource` targeting a file on the server."""

    def __init__(self, server_path: str):
        """Create a new ServerPathResource.

        Args:
            server_path (str): the path on the server to target.
        """
        super().__init__(server_path, type_utils.path_to_extension(server_path))

    @property
    def template_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "template_type": self.filetype,
            "filename": self.data,
        }

    @property
    def secondary_file_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "filename": self.data,
        }


class URLResource(Resource):
    """A `Resource` targeting a file at a URL."""

    def __init__(self, url: str, filetype: str):
        """Create a new URLResource.

        Args:
            url (str): the URL location of the file.
            filetype (str): the file type (extension).
        """
        super().__init__(url, filetype)

    @property
    def template_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "template_type": self.filetype,
            "url": self.data,
        }

    @property
    def secondary_file_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "file_url": self.data,
        }


class HTMLResource(Resource):
    """A Resource containing HTML data in plain text."""

    def __init__(
        self,
        htmlstring: str,
        landscape: bool = False,
    ):
        """Create a new HTMLResource.

        Args:
            htmlstring (str): the HTML input in plain text.
            landscape (bool, optional): whether the HTML should be rendered as landscape-oriented page. Defaults to False.
        """
        super().__init__(htmlstring, "html")
        self.landscape: bool = landscape

    @property
    def orientation(self) -> str:
        """Either None or `"landscape"`, as is passed in the JSON.

        If `"landscape"`, the HTML is rendered as landscape-oriented page.
        Orientation is not supported for prepend/append sources, only for template resources.

        Returns:
            str: the orientation.
        """
        return None if not self.landscape else "landscape"

    @property
    def template_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "template_type": self.filetype,
            "html_template_content": self.data,
            "orientation": self.orientation,
        }

    @property
    def secondary_file_dict(self) -> Dict:
        """
        Returns:
            str: the JSON representation of this resource.
        """
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "file_content": self.data,
        }
