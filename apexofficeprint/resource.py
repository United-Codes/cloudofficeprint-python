import base64
import json
from .aop_utils import type_utils
from os import path
from urllib.parse import urlparse
from enum import Enum


class DataType(Enum):
    """An enum for data types."""
    RAW = 1
    BASE64 = 2
    URL = 3
    SERVER_PATH = 4
    HTML = 5


class Resource:
    def __init__(self, datatype=None, data=None, filetype=None, orientation=None):
        """This constructor is not meant to be used directly."""
        self._datatype = datatype
        self._data = data
        self.filetype = filetype  # use the setter
        self._orientation = orientation

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
    def datatype(self) -> DataType:
        """The type of data this AOPResource contains.

        Returns:
            DataType: data type
        """
        return self._datatype

    @property
    def data(self):
        """The data contained in this AOPResource.

        Can be:
        - an url
        - raw data
        - a base64 string
        - an html string
        - a path on the server
        based on datatype
        """
        return self._data

    @property
    def orientation(self) -> str:
        """Either None or "landscape", as is passed in the json.

        Orientation is not supported for prepend/append sources, only for template resources.

        Returns:
            str: orientation
        """
        return self._orientation

    @property
    def data_base64(self) -> str:
        """Get the base64 value of this AOPResource.

        If the data type is BASE64, just returns the data.
        When the data type is RAW, converts to base64.
        For any other data type, returns None.

        Returns:
            str: base64 string
        """
        if (self.datatype is DataType.BASE64):
            return self.data
        elif (self.datatype is DataType.RAW):
            return base64.b64encode(self.data).decode("ascii")
        else:
            return None

    @property
    def template_json(self) -> str:
        """Get the json representation when used as a template.

        Returns:
            str: json string
        """
        return json.dumps(self.template_dict)

    @property
    def template_dict(self) -> dict:
        """Convert this Resource object to a dict object for use as a template.

        This dict and the template json representation are isomorphic.

        Returns:
            dict: template dict representation of this Resource
        """
        result = {
            "template_type": self.filetype  # filetype should always be present
        }

        base64string = self.data_base64
        if base64string is not None:
            result["file"] = base64string
        elif self.datatype is DataType.URL:
            result["url"] = self.data
        elif self.datatype is DataType.HTML:
            result["html_template_content"] = self.data
            result["orientation"] = self.orientation
        elif self.datatype is DataType.SERVER_PATH:
            result["filename"] = self.data

        return result

    @property
    def concatfile_json(self) -> str:
        """Get the json representation for use as a prepend or append file.

        Returns:
            str: json string
        """
        return json.dumps(self.concatfile_dict)

    @property
    def concatfile_dict(self) -> dict:
        """Convert this Resource object to a dict object for use as a prepend or append file.

        This dict and the "concat file" json representation are isomorphic.

        Returns:
            dict: prepend/append representation of this Resource
        """
        result = {
            "mime_type": type_utils.extension_to_mimetype(self.filetype)
        }

        base64string = self.data_base64
        if base64string is not None:
            result["file_source"] = "base64"
            result["file_content"] = base64string
        elif self.datatype is DataType.URL:
            result["file_source"] = "url"
            result["file_url"] = self.data
        elif self.datatype is DataType.HTML:
            result["file_source"] = "plain"
            result["file_content"] = self.data
        elif self.datatype is DataType.SERVER_PATH:
            result["file_source"] = "file"
            result["filename"] = self.data

        return result

    def __str__(self):
        """Override the string representation of this class to return the template-style json."""
        return self.template_json

    @classmethod
    def from_base64(cls, base64string: str, filetype: str) -> 'Resource':
        """Create a Resource from a base64 string and a file type (extension).

        Args:
            base64string (str): base64 encoded string
            filetype (str): file type (extension)

        Returns:
            Resource: the created Resource
        """
        return cls(datatype=DataType.BASE64, data=base64string, filetype=filetype)

    @classmethod
    def from_raw(cls, raw_data, filetype: str) -> 'Resource':
        """Create a Resource from raw file data and a file type (extension).

        Args:
            raw_data: raw data as a bytes-like object
                      (https://docs.python.org/3/glossary.html#term-bytes-like-object)
            filetype (str): file type (extension)

        Returns:
            Resource: the created Resource
        """
        return cls(datatype=DataType.RAW, data=raw_data, filetype=filetype)

    @classmethod
    def from_local_file(cls, path: str) -> 'Resource':
        """Create a Resource targeting a local file.

        The local file is read and its data is stored in the resulting AOPResource.
        Throws IOError if it can't read the file.
        If filetype is not given, use the extension from the file path.

        Args:
            path (str): path to local file

        Returns:
            Resource: the created Resource
        """
        f = open(path, "rb")
        file_content = f.read()
        f.close()
        return cls(
            data=file_content,
            datatype=DataType.RAW,
            filetype=path.splitext(path)[1]
        )

    @classmethod
    def from_server_path(cls, path: str) -> 'Resource':
        """Create an AOPResource targeting a file on the server.

        If filetype is not given, use the extension from the file path.

        Args:
            path (str): location of target file on the server

        Returns:
            Resource: the created Resource
        """
        return cls(data=path, filetype=path.splitext(path)[1])

    @classmethod
    def from_url(cls, url: str, filetype: str) -> 'Resource':
        """Create an AOPResource targeting the file at url with given filetype (extension).

        Args:
            url (str): file url
            filetype (str): file type (extension)

        Returns:
            Resource: the created Resource
        """
        return cls(data=url, datatype=DataType.URL, filetype=filetype)

    @classmethod
    def from_html(cls, htmlstring: str, landscape: bool = False) -> 'Resource':
        """Create an AOPResource with html data in plain text.

        Landscape is not supported for prepend/append sources, only for template resources.

        Args:
            htmlstring (str): html content
            landscape (bool, optional): whether to use the landscape option. Defaults to False.

        Returns:
            Resource: the created Resource
        """
        orientation = "landscape" if landscape else None
        return cls(data=htmlstring, datatype=DataType.HTML, filetype="html", orientation=orientation)

    @staticmethod
    def is_supported_resource_type(type_: str) -> bool:
        """Check if the given resource type is a supported resource type.

        Args:
            type_ (str): resource type (extension)

        Returns:
            bool: whether the given resource type is a supported resource type
        """
        return type_ in type_utils.supported_resource_types
