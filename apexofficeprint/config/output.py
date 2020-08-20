import json
from .cloud import CloudAccessToken
from .pdf import PDFOptions

class OutputConfig:
    """Class to specify output configuration for a request.

    This configuration is general and for the entire list of output files.
    """

    def __init__(self,
                 filetype: str = None,
                 encoding: str = "raw",
                 converter: str = "libreoffice",
                 cloud_access_token: 'CloudAccessToken' = None,
                 server_directory: str = None,
                 pdf_options: 'PDFOptions' = None):
        """
        Args:
            filetype (str, optional): `OutputConfig.filetype`. Defaults to None.
            encoding (str, optional): `OutputConfig.encoding`. Defaults to "raw".
            converter (str, optional): `OutputConfig.converter`. Defaults to "libreoffice".
            cloud_access_token (CloudAccessToken, optional): `OutputConfig.cloud_access_token`. Defaults to None.
            server_directory (str, optional): `OutputConfig.server_directory`. Defaults to None.
            pdf_options (PDFOptions, optional): `OutputConfig.pdf_options`. Defaults to None.
        """
        self.filetype: str = filetype
        """The file type (as extension) to use for the output."""
        self.converter: str = converter
        """The pdf converter to use.

        Can be "libreoffice", "officetopdf" or any custom defined converter.
        Custom converters are configurated in the AOP server's `aop_config.json` file.
        """
        self.cloud_access_token: CloudAccessToken = cloud_access_token
        """Access token used to access various cloud services for output storage."""
        self.server_directory: str = server_directory
        """Base directory to save output files into.

        Can only be used if the server allows to save on disk.
        The specific output path for each file is appended to the base path.
        """
        self.pdf_options: PDFOptions = pdf_options
        """Optional PDF options."""

        self.encoding = encoding

    @property
    def json(self) -> str:
        """The json representation of this output config.

        This is the json serialization of the dict representation.
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """The dict representation of this output config."""
        result = {
            "output_encoding": self._encoding,
            "output_converter": self.converter
        }

        if self.filetype is not None:
            result["output_type"] = self.filetype
        if self.cloud_access_token is not None:
            result.update(self.cloud_access_token.as_dict)
        if self.server_directory is not None:
            result["output_directory"] = self.server_directory
        if self.pdf_options is not None:
            result.update(self.pdf_options)

        return result

    @property
    def encoding(self) -> str:
        """The encoding to use, either "raw" or "base64"."""
        return self._encoding

    @encoding.setter
    def encoding(self, value: str):
        if not (value == "raw" or value == "base64"):
            raise ValueError(
                f'Encoding must be either "raw" or "base64", was "{value}".')
        self._encoding = value