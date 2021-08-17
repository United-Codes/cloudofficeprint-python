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
from .own_utils import type_utils, file_utils
from abc import abstractmethod, ABC


class Resource(ABC):
    """The abstract base class for the resources."""

    def __init__(self, data: Union[str, bytes] = None, filetype: str = None):
        """
        Args:
            data (Union[str, bytes], optional): the data for this resource. Defaults to None.
            filetype (str, optional): the file type of this resource. Defaults to None.
        """
        self._data: Union[str, bytes] = data
        self.filetype: str = filetype

    @property
    def mimetype(self) -> str:
        """Resource type as a mime type.

        Returns:
            str: resource type as a mime type
        """
        return type_utils.extension_to_mimetype(self.filetype)

    @property
    def data(self) -> Union[str, bytes]:
        """The data contained in this Resource.

        Returns:
            Union[str, bytes]: the data contained in this Resource
        """
        return self._data

    @property
    def template_json(self) -> str:
        """Get the JSON representation when used as a template.

        Returns:
            str: JSON representation of this resource as a template
        """
        return json.dumps(self.template_dict)

    @property
    @abstractmethod
    def template_dict(self) -> Dict:
        """This Resource object as a dict object for use as a template.
        This dict and the template JSON representation (`Resource.template_json`) are isomorphic.

        Returns:
            Dict: dict representation of this resource as a template
        """
        pass

    @property
    def secondary_file_json(self) -> str:
        """The JSON representation for use as secondary file.

        Returns:
            str: JSON representation of this resource as a secondary file
        """
        return json.dumps(self.secondary_file_dict)

    @property
    @abstractmethod
    def secondary_file_dict(self) -> Dict:
        """This Resource object as a dict object for use as a secondary file (prepend, append, insert, as subtemplate).
        This dict and the "concat file" JSON representation (`Resource.secondary_file_json`) are isomorphic.

        Returns:
            Dict: dict representation of this resource as a secondary file
        """
        pass

    def __str__(self) -> str:
        """Override the string representation of this class to return the template-style json.

        Returns:
            str: JSON representation of this resource as a template
        """
        return self.template_json

    @staticmethod
    def from_base64(base64string: str, filetype: str) -> 'Base64Resource':
        """Create a Base64Resource from a base64 string and a file type (extension).

        Args:
            base64string (str): base64 encoded string
            filetype (str): file type (extension)

        Returns:
            Base64Resource: the created Resource
        """
        return Base64Resource(base64string, filetype)

    @staticmethod
    def from_raw(raw_data: bytes, filetype: str) -> 'RawResource':
        """Create a RawResource from raw file data and a file type (extension).

        Args:
            raw_data (bytes): raw data as a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object)
            filetype (str): file type (extension)

        Returns:
            RawResource: the created Resource
        """
        return RawResource(raw_data, filetype)

    @staticmethod
    def from_local_file(local_path: str) -> 'Base64Resource':
        """Create a Base64Resource with the contents of a local file.

        Throws IOError if it can't read the file.
        The filetype is determined by the extension of the file.

        Args:
            local_path (str): path to local file

        Returns:
            Base64Resource: the created Resource
        """
        base64string: str = file_utils.read_file_as_base64(local_path)
        return Base64Resource(base64string, type_utils.path_to_extension(local_path))

    @staticmethod
    def from_server_path(path: str) -> 'ServerPathResource':
        """Create a ServerPathResource targeting a file on the server.

        The filetype is determined by the extension of the file.

        Args:
            path (str): location of target file on the server

        Returns:
            ServerPathResource: the created Resource
        """
        return ServerPathResource(path)

    @staticmethod
    def from_url(url: str, filetype: str) -> 'URLResource':
        """Create an Resource targeting the file at url with given filetype (extension).

        Args:
            url (str): file url
            filetype (str): file type (extension)

        Returns:
            URLResource: the created Resource
        """
        return URLResource(url, filetype)

    @staticmethod
    def from_html(htmlstring: str, landscape: bool = False) -> 'HTMLResource':
        """Create an HTMLResource with html data in plain text.

        Landscape is not supported for prepend/append sources, only for template resources.

        Args:
            htmlstring (str): html content
            landscape (bool, optional): whether to use the landscape option. Defaults to False.

        Returns:
            HTMLResource: the created Resource
        """
        return HTMLResource(htmlstring, landscape)


class RawResource(Resource):
    """A `Resource` containing raw binary data."""

    def __init__(self, raw_data: bytes, filetype: str):
        """
        Args:
            raw_data (bytes): raw data as a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object)
            filetype (str): file type (extension)
        """
        super().__init__(raw_data, filetype)

    @property
    def base64(self) -> str:
        """Base64 representation of the raw data in `RawResource.data`.

        Returns:
            str: base64 representation of the raw data in `RawResource.data`
        """
        return file_utils.raw_to_base64(self.data)

    @property
    def template_dict(self) -> Dict:
        return {
            "template_type": self.filetype,
            "file": self.base64
        }

    @property
    def secondary_file_dict(self) -> Dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "base64",
            "file_content": self.base64
        }


class Base64Resource(Resource):
    """A `Resource` containing base64 data."""

    def __init__(self, base64string: str, filetype: str):
        """
        Args:
            base64string (str): base64 encoded file
            filetype (str): file type (extension)
        """
        super().__init__(base64string, filetype)

    @property
    def template_dict(self) -> Dict:
        return {
            "template_type": self.filetype,
            "file": self.data
        }

    @property
    def secondary_file_dict(self) -> Dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "base64",
            "file_content": self.data
        }


class ServerPathResource(Resource):
    """A `Resource` targeting a file on the server."""

    def __init__(self, server_path: str):
        """
        Args:
            server_path (str): path on the server to target
        """
        super().__init__(server_path, type_utils.path_to_extension(server_path))

    @property
    def template_dict(self) -> Dict:
        return {
            "template_type": self.filetype,
            "filename": self.data
        }

    @property
    def secondary_file_dict(self) -> Dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "filename": self.data
        }


class URLResource(Resource):
    """A `Resource` targeting a file at a URL."""

    def __init__(self, url: str, filetype: str):
        """
        Args:
            url (str): URL location of the file
            filetype (str): file type (extension)
        """
        super().__init__(url, filetype)

    @property
    def template_dict(self) -> Dict:
        return {
            "template_type": self.filetype,
            "url": self.data
        }

    @property
    def secondary_file_dict(self) -> Dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "file_url": self.data
        }


class HTMLResource(Resource):
    """A Resource containing HTML data in plain text."""

    def __init__(self, htmlstring: str, landscape: bool = False):
        """
        Args:
            htmlstring (str): HTML input in plain text
            landscape (bool, optional): Whether the HTML should be rendered as landscape-oriented page. Defaults to False.
        """
        super().__init__(htmlstring, "html")
        self.landscape: bool = landscape

    @property
    def orientation(self) -> str:
        """Either None or `"landscape"`, as is passed in the JSON.

        If `"landscape"`, the HTML is rendered as landscape-oriented page.
        Orientation is not supported for prepend/append sources, only for template resources.

        Returns:
            str: orientation
        """
        return None if not self.landscape else "landscape"

    @property
    def template_dict(self) -> Dict:
        result = {
            "template_type": self.filetype,
            "html_template_content": self.data
        }

        if self.orientation is not None:
            result["orientation"] = self.orientation

        return result

    @property
    def secondary_file_dict(self) -> Dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "file_content": self.data
        }
