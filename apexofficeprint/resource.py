import base64
import json
from .aop_utils import type_utils
from os import path
from urllib.parse import urlparse
from enum import Enum


class DataType(Enum):
    """
    An enum for data types.
    """
    RAW = 1
    BASE64 = 2
    URL = 3
    SERVER_PATH = 4
    HTML = 5


class Resource:
    def __init__(self, datatype=None, data=None, filetype=None, orientation=None):
        """
        This constructor is not meant to be used directly.
        """
        self._datatype = datatype
        self._data = data
        self.filetype = filetype  # use the setter
        self._orientation = orientation

    @property
    def filetype(self):
        """
        Resource type as an extension.
        """
        return self._filetype

    @filetype.setter
    def filetype(self, value):
        """
        Setter for filetype, checks if the type is supported.
        """
        if self.is_supported_resource_type(value):
            self._filetype = value
        else:
            raise TypeError(f'Unsupported template type: "{value}"')

    @property
    def datatype(self):
        """
        The type of data this AOPResource contains.
        A value from DataType(Enum).
        """
        return self._datatype

    @property
    def data(self):
        """
        The data contained in this AOPResource.
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
    def orientation(self):
        """
        Either None or "landscape", as is passed in the json.
        Orientation is not supported for prepend/append sources, only for template resources.
        """
        return self._orientation

    @property
    def data_base64(self):
        """
        Get the base64 value of this AOPResource.
        If the data type is BASE64, just returns the data.
        When the data type is RAW, converts to base64.
        For any other data type, returns None.
        """
        if (self.datatype is DataType.BASE64):
            return self.data
        elif (self.datatype is DataType.RAW):
            return base64.b64encode(self.data).decode("ascii")
        else:
            return None

    @property
    def template_json(self):
        """
        Get the json representation when used as a template.
        """
        return json.dumps(self.template_dict)

    @property
    def template_dict(self):
        """
        Convert this AOPResource object to a dict object for use as a template.
        This dict and the template json representation are isomorphic.
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
    def concatfile_json(self):
        """
        Get the json representation for use as a prepend or append file.
        """
        return json.dumps(self.concatfile_dict)

    @property
    def concatfile_dict(self):
        """
        Convert this AOPResource object to a dict object for use as a prepend or append file.
        This dict and the "concat file" json representation are isomorphic.
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
        """
        Override the string representation of this class to return the template-style json.
        """
        return self.template_json

    @classmethod
    def from_base64(cls, base64string, filetype):
        """
        Create an AOPResource from a base64 string and a file type (extension).
        """
        return cls(datatype=DataType.BASE64, data=base64string, filetype=filetype)

    @classmethod
    def from_raw(cls, raw_data, filetype):
        """
        Create an AOPResource from raw file data and a file type (extension).
        The raw data should be a bytes-like object (https://docs.python.org/3/glossary.html#term-bytes-like-object).
        """
        return cls(datatype=DataType.RAW, data=raw_data, filetype=filetype)

    @classmethod
    def from_local_file(cls, local_file_path, filetype=None):
        """
        Create an AOPResource targeting a local file.
        The local file is read and its data is stored in the resulting AOPResource.
        Throws IOError if it can't read the file.
        """
        if filetype is None:
            filetype = path.splitext(local_file_path)[1]
        f = open(local_file_path, "rb")
        file_content = f.read()
        f.close()
        return cls(
            data=file_content,
            datatype=DataType.RAW,
            filetype=filetype
        )

    @classmethod
    def from_server_path(cls, path, filetype):
        """
        Create an AOPResource targeting a file on the server.
        """
        return cls(data=path, filetype=filetype)

    @classmethod
    def from_url(cls, url, filetype):
        """
        Create an AOPResource targeting the file at url with given filetype (extension).
        """
        return cls(data=url, datatype=DataType.URL, filetype=filetype)

    @classmethod
    def from_html(cls, htmlstring, landscape=False):
        """
        Create an AOPResource with html data in plain text.
        Landscape is not supported for prepend/append sources, only for template resources.
        """
        orientation = "landscape" if landscape else None
        return cls(data=htmlstring, datatype=DataType.HTML, filetype="html", orientation=orientation)

    @staticmethod
    def is_supported_resource_type(type_):
        return type_ in type_utils.supported_resource_types
