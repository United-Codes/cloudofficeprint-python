import json
from typing import Dict, List, Mapping
from .cloud import CloudAccessToken
from .pdf import PDFOptions


class RequestOption:
    """
    Class for a request option of the output,
    if this is specified then COP makes a call to the given option with response/output of the current request.
    """

    def __init__(self,
                 url: str,
                 headers: Mapping[str, str] = None,
                 ):
        """
        Args:
            url (str): the URL to which the output/response will be posted.
            headers (Mapping): Any additional information to be included for the header. Defaults to None.
        """
        self.url: str = url
        self.headers: Mapping[str, str] = headers

    @property
    def as_dict(self) -> Dict:
        """The dict representation of this request option.

        Returns:
            Dict: the dict representation of this request option
        """
        result = {
            "url": self.url,
        }

        if self.headers is not None:
            result["extra_headers"] = self.headers

        return result


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
                 prepend_per_page: bool = None,
                 append_per_page: bool = None,
                 request_option: RequestOption = None,
                 ):
        """
        Args:
            filetype (str, optional): The file type (as extension) to use for the output. Defaults to None (set to template-type in printjob.py).
            encoding (str, optional): Encoding of output file. Either "raw" or "base64". Defaults to "raw".
            converter (str, optional): The pdf converter to use. Can be "libreoffice", "officetopdf" or any custom defined converter. Custom converters are configurated in the Cloud Office Print server's `aop_config.json` file. Defaults to "libreoffice".
            cloud_access_token (CloudAccessToken, optional): Access token used to access various cloud services for output storage. Defaults to None.
            server_directory (str, optional): Base directory to save output files into. Can only be used if the server allows to save on disk. The specific output path for each file is appended to the base path. Defaults to None.
            pdf_options (PDFOptions, optional): Optional PDF options. Defaults to None.
            prepend_per_page (bool, optional): Ability to prepend file before each page of output. Defaults to None.
            append_per_page (bool, optional): Ability to append file after each page of output. Defaults to None.
            request_option (RequestOption): The request option, if this is specified then COP makes a call to the given option with response/output of the current request. Defaults to None.
        """
        self.filetype: str = filetype
        self.converter: str = converter
        self.cloud_access_token: CloudAccessToken = cloud_access_token
        self.server_directory: str = server_directory
        self.pdf_options: PDFOptions = pdf_options
        self.encoding = encoding
        self.prepend_per_page = prepend_per_page
        self.append_per_page = append_per_page
        self.request_option: RequestOption = request_option

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
        if self.prepend_per_page is not None:
            result["output_prepend_per_page"] = self.prepend_per_page
        if self.append_per_page is not None:
            result["output_append_per_page"] = self.append_per_page
        if self.request_option is not None:
            result["request_option"] = self.request_option.as_dict
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
