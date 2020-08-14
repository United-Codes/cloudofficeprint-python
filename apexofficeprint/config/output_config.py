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
                 server_directory: str = None,
                 pdf_options: PDFOptions = None):
        self._filetype = filetype
        self._encoding = encoding
        self._converter = converter
        self._cloud_access_token = cloud_access_token
        self._server_directory = server_directory
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
        if self._server_directory is not None:
            result["output_directory"] = self._server_directory
        if self._pdf_options is not None:
            result.update(self._pdf_options)
        
        return result

    @property
    def filetype(self) -> str:
        """The file type (as extension) to use for the output.

        Returns:
            str: filetype
        """
        return self._filetype

    @filetype.setter
    def filetype(self, value: str):
        """Set filetype

        Args:
            value (str): filetype
        """
        self._filetype = value

    @property
    def encoding(self) -> str:
        """The encoding to use, either "raw" or "base64".

        Returns:
            str: encoding
        """
        return self._encoding

    @encoding.setter
    def encoding(self, value: str):
        """Set encoding.

        Args:
            value (str): encoding
        """
        if not (value == "raw" or value == "base64"):
            raise ValueError(f'Encoding must be either "raw" or "base64", was "{value}".')
        self._encoding = value

    @property
    def converter(self) -> str:
        """The pdf converter to use.

        Can be "libreoffice", "officetopdf" or any custom defined converter.
        Custom converters are configurated in the AOP server's `aop_config.json` file.

        Returns:
            str: PDF converter name
        """
        return self._converter

    @converter.setter
    def converter(self, value: str):
        """Set converter

        Args:
            value (str): PDF converter name
        """
        self._converter = value

    @property
    def cloud_access_token(self) -> CloudAccessToken:
        """Access token used to access various cloud services for output storage.

        It should be an instance of apexofficeprint.CloudAccessToken.

        Returns:
            CloudAccessToken: access token
        """
        return self._cloud_access_token

    @cloud_access_token.setter
    def cloud_access_token(self, value: CloudAccessToken):
        """Set cloud_access_token

        Args:
            value (CloudAccessToken): cloud_access_token
        """
        self._cloud_access_token = value

    @property
    def server_directory(self) -> str:
        """Base directory to save output files into if the server allows save on disk.

        The specific output path for each file is appended to the base path.

        Returns:
            str: path to the base directory on the server
        """
        return self._server_directory

    @server_directory.setter
    def server_directory(self, value: str):
        """Set server_directory

        Args:
            value (str): server_directory
        """
        self._server_directory = value

    @property
    def pdf_options(self) -> PDFOptions:
        """Optional PDF options.

        Should be an instance of apexofficeprint.PDFOptions

        Returns:
            PDFOptions: PDF options
        """
        return self._pdf_options

    @pdf_options.setter
    def pdf_options(self, value: PDFOptions):
        """Set pdf_options

        Args:
            value (PDFOptions): pdf_options
        """
        self._pdf_options = value
