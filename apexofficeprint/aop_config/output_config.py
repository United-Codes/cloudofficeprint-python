from .cloud_access_token import CloudAccessToken
from .pdf_options import PDFOptions
import json


class OutputConfig:
    """Class to specify output configuration for a request.

    This configuration is general and for the entire list of output files.
    """

    def __init__(self,
                 filetype: str = None,
                 encoding: str = "raw",
                 converter: str = "libreoffice",
                 cloud_access_token: CloudAccessToken = None,
                 server_location: str = None,
                 pdf_options: PDFOptions = None):
        self._filetype = filetype
        self._encoding = encoding
        self._converter = converter
        self._cloud_access_token = cloud_access_token
        self._server_location = server_location
        self._pdf_options = pdf_options

    @property
    def json(self) -> str:
        """The json representation of this output config.

        This is the json serialization of the dict representation.

        Returns:
            str: json representation
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """The dict representation of this output config.

        Returns:
            dict: dict representation
        """
        result = {
            "output_encoding": self._encoding,
            "output_converter": self._converter
        }
        if self._filetype is not None:
            result["output_type"] = self._filetype
        if self._cloud_access_token is not None:
            result.update(self._cloud_access_token.as_dict)
        if self._server_location is not None:
            result["output_directory"] = self._server_location
        if self._pdf_options is not None:
            result.update(self._pdf_options)

    # TODO: docstrings
    @property
    def filetype(self) -> str:
        return self._filetype

    @filetype.setter
    def filetype(self, value: str):
        self._filetype = value

    @property
    def encoding(self) -> str:
        return self._encoding

    @encoding.setter
    def encoding(self, value: str):
        self._encoding = value

    @property
    def converter(self) -> str:
        return self._converter

    @converter.setter
    def converter(self, value: str):
        self._converter = value

    @property
    def cloud_access_token(self) -> CloudAccessToken:
        return self._cloud_access_token

    @cloud_access_token.setter
    def cloud_access_token(self, value: CloudAccessToken):
        self._cloud_access_token = value

    @property
    def server_location(self) -> str:
        return self._server_location

    @server_location.setter
    def server_location(self, value: str):
        self._server_location = value

    @property
    def pdf_options(self) -> PDFOptions:
        return self._pdf_options

    @pdf_options.setter
    def pdf_options(self, value: PDFOptions):
        self._pdf_options = value
