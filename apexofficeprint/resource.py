"""
Module containing the Resource class and its subclasses, which is also exposed at package level.

Every resource contains or points to a file to be used as a template or to be included as an append/prepend document (in case of pdf output).

## Resource creation

`Resource` is the base class which should not be constructed.
The recommended way of obtaining a `Resource` is through the static from_... methods (e.g. `Resource.from_local_file`),
alternatively, the `Resource` subclasses can be constructed to form a valid `Resource`.
"""

import json
import base64
from ._utils import type_utils
from abc import abstractmethod


class Resource():
    """The base class for the resources."""

    def __init__(self, data=None, filetype=None):
        self._data = data
        self.filetype = filetype  # use the setter

    @property
    def mimetype(self) -> str:
        """Resource type as a mime type"""
        return type_utils.extension_to_mimetype(self.filetype)

    @property
    def filetype(self) -> str:
        """Resource type as an extension (e.g. "docx")."""
        return self._filetype

    @filetype.setter
    def filetype(self, value: str):
        """Setter for filetype, checks if the type is supported.

        Raises:
            TypeError: the given type is not a supported resource type.
        """
        if self.is_supported_resource_type(value):
            self._filetype = value
        else:
            raise TypeError(f'Unsupported template type: "{value}"')

    @property
    def data(self):
        """The data contained in this AOPResource."""
        return self._data

    @property
    def template_json(self) -> str:
        """Get the json representation when used as a template.

        Returns:
            str: json string
        """
        return json.dumps(self.template_dict)

    @property
    @abstractmethod
    def template_dict(self) -> dict:
        """Convert this Resource object to a dict object for use as a template.

        Should be overridden by all subclasses.
        This dict and the template json representation (`Resource.template_json`) are isomorphic.

        Returns:
            dict: template dict representation of this Resource
        """
        pass

    @property
    def concatfile_json(self) -> str:
        """Get the json representation for use as a prepend or append file.

        Returns:
            str: json string
        """
        return json.dumps(self.concatfile_dict)

    @property
    @abstractmethod
    def concatfile_dict(self) -> dict:
        """Convert this Resource object to a dict object for use as a prepend or append file.

        Should be overridden by all subclasses.
        This dict and the "concat file" json representation (`Resource.concatfile_json`) are isomorphic.

        Returns:
            dict: prepend/append representation of this Resource
        """
        pass

    def __str__(self):
        """Override the string representation of this class to return the template-style json."""
        return self.template_json

    @staticmethod
    def from_base64(base64string: str, filetype: str) -> 'Base64Resource':
        """Create a Resource from a base64 string and a file type (extension).

        Args:
            base64string (str): base64 encoded string
            filetype (str): file type (extension)

        Returns:
            Base64Resource: the created Resource
        """
        return Base64Resource(base64string, filetype)

    @staticmethod
    def from_raw(raw_data, filetype: str) -> 'RawResource':
        """Create a RawResource from raw file data and a file type (extension).

        Args:
            raw_data: raw data as a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object)
            filetype (str): file type (extension)

        Returns:
            RawResource: the created Resource
        """
        return RawResource(raw_data, filetype)

    @staticmethod
    def from_local_file(local_path: str) -> 'RawResource':
        """Create a RawResource with the contents of a local file.

        Throws IOError if it can't read the file.
        The filetype is determined by the extension of the file.

        Args:
            local_path (str): path to local file

        Returns:
            RawResource: the created Resource
        """
        f = open(local_path, "rb")
        file_content = f.read()
        f.close()
        # [1] for the extension with leading ".", [1:] to cut off the dot
        return RawResource(file_content, type_utils.path_to_extension(local_path))

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
        """Create an AOPResource targeting the file at url with given filetype (extension).

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

    @staticmethod
    def is_supported_resource_type(type_: str) -> bool:
        """Check if the given resource type is a supported resource type.

        Args:
            type_ (str): resource type (extension)

        Returns:
            bool: whether the given resource type is a supported resource type
        """
        return type_ in type_utils.supported_resource_types


class RawResource(Resource):
    """A Resource containing raw binary data."""

    def __init__(self, raw_data, filetype):
        super().__init__(raw_data, filetype)

    @property
    def base64(self):
        return base64.b64encode(self.data).decode("ascii")

    @property
    def template_dict(self) -> dict:
        return {
            "template_type": self.filetype,
            "file": self.base64
        }

    @property
    def concatfile_dict(self) -> dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "base64",
            "file_content": self.base64
        }


class Base64Resource(Resource):
    """A Resource containing base64 data."""

    def __init__(self, base64string, filetype):
        super().__init__(base64string, filetype)

    @property
    def template_dict(self) -> dict:
        return {
            "template_type": self.filetype,
            "file": self.data
        }

    @property
    def concatfile_dict(self) -> dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "base64",
            "file_content": self.data
        }


class ServerPathResource(Resource):
    """A Resource targeting a file on the server."""

    def __init__(self, server_path):
        super().__init__(server_path, type_utils.path_to_extension(server_path))

    @property
    def path(self):
        return self.data

    @property
    def template_dict(self) -> dict:
        return {
            "template_type": self.filetype,
            "filename": self.data
        }

    @property
    def concatfile_dict(self) -> dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "filename": self.data
        }


class URLResource(Resource):
    """A Resource targeting a file at an URL."""

    def __init__(self, url, filetype):
        super().__init__(url, filetype)

    @property
    def template_dict(self) -> dict:
        return {
            "template_type": self.filetype,
            "url": self.data
        }

    @property
    def concatfile_dict(self) -> dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "file_url": self.data
        }


class HTMLResource(Resource):
    """A Resource containing HTML data in plain text."""

    def __init__(self, htmlstring: str, landscape: bool = False):
        super().__init__(htmlstring, "html")
        self._landscape = landscape

    @property
    def orientation(self) -> str:
        """Either None or "landscape", as is passed in the json.

        Orientation is not supported for prepend/append sources, only for template resources.

        Returns:
            str: orientation
        """
        return None if not self._landscape else "landscape"

    @property
    def landscape(self):
        """Whether this HTMLResource should be passed with the landscape option."""
        return self._landscape

    @property
    def template_dict(self) -> dict:
        result = {
            "template_type": self.filetype,
            "html_template_content": self.data
        }

        if self.orientation is not None:
            result["orientation"] = self.orientation

        return result

    @property
    def concatfile_dict(self) -> dict:
        return {
            "mime_type": self.mimetype,
            "file_source": "file",
            "file_content": self.data
        }
