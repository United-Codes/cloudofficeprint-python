import json
from typing import Dict
from .cloud import CloudAccessToken
from .pdf import PDFOptions
from .request_option import requestOptions


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
                 pdf_options: PDFOptions = None,
                 append_per_page: bool = None,
                 prepend_per_page: bool = None,
                 output_polling: bool = None,
                 secret_key: str = None,
                 request_option: requestOptions = None):
        """
        Args:
            filetype (str, optional): The file type (as extension) to use for the output. Defaults to None (set to template-type in printjob.py).
            encoding (str, optional): Encoding of output file. Either "raw" or "base64". Defaults to "raw".
            converter (str, optional): The pdf converter to use. Can be "libreoffice", "officetopdf" or any custom defined converter. Custom converters are configurated in the Cloud Office Print server's `aop_config.json` file. Defaults to "libreoffice".
            cloud_access_token (CloudAccessToken, optional): Access token used to access various cloud services for output storage. Defaults to None.
            server_directory (str, optional): Base directory to save output files into. Can only be used if the server allows to save on disk. The specific output path for each file is appended to the base path. Defaults to None.
            pdf_options (PDFOptions, optional): Optional PDF options. Defaults to None.
            append_per_page (bool, optional): Ability to append file after each page of output.
            prepend_per_page(bool, optional):  Ability to prepend file after each page of output.
            output_polling(str, optional):  A unique link for each request is sent back, which can be used later to download the output file.
            secret_key(str, optional): A secret key can be specified to encrypt the file stored on the server (ussed with output polling).
            request_option(requestOptions, optional): AOP makes a call to the given option with response/output of the current request.
        """
        self.filetype: str = filetype
        self.converter: str = converter
        self.cloud_access_token: CloudAccessToken = cloud_access_token
        self.server_directory: str = server_directory
        self.pdf_options: PDFOptions = pdf_options
        self.encoding = encoding
        self.append_per_page = append_per_page
        self.prepend_per_page = prepend_per_page
        self.output_polling = output_polling
        self.secret_key = secret_key
        self.request_option = request_option

    @property
    def json(self) -> str:
        """The JSON representation of this output config.

        This is the JSON serialization of the dict representation.

        Returns:
            str: JSON representation of this output config
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> Dict:
        """The dict representation of this output config.

        Returns:
            Dict: the dict representation of this output config
        """
        result = {
            "output_encoding": self._encoding,
            "output_converter": self.converter,
        }

        if self.filetype is not None:
            result['output_type'] = self.filetype
        if self.cloud_access_token is not None:
            result.update(self.cloud_access_token.as_dict)
        if self.server_directory is not None:
            result["output_directory"] = self.server_directory
        if self.pdf_options is not None:
            result.update(self.pdf_options.as_dict)
        if self.append_per_page is not None:
            result["output_append_per_page"] = self.append_per_page
        if self.prepend_per_page is not None:
            result["output_prepend_per_page"] = self.prepend_per_page
        if self.output_polling is not None:
            result['output_polling'] = self.output_polling
        if self.secret_key is not None:
            result['secret_key'] = self.secret_key
        if self.request_option is not None:
            result['request_option'] = self.request_option.as_dict
        return result

    @property
    def encoding(self) -> str:
        """The encoding to use, either "raw" or "base64".

        Returns:
            str: the encoding to use, either "raw" or "base64"
        """
        return self._encoding

    @encoding.setter
    def encoding(self, value: str):
        """Setter for the encoding to use

        Args:
            value (str): encoding to use

        Raises:
            ValueError: raise an error when the given encoding is not supported
        """
        if not (value == "raw" or value == "base64"):
            raise ValueError(
                f'Encoding must be either "raw" or "base64", was "{value}".')
        self._encoding = value
