"""
Module for output configurations.

The classes under this module encapsulate various configuration options for a print job.
They are to be used with `job.PrintJob`.
"""

from typing import List, Union
from abc import abstractmethod
import json
import requests
import logging
import re
from urllib.parse import urljoin, urlparse

SERVICES = [
    "dropbox",
    "gdrive",
    "onedrive",
    "aws_s3",
    "sftp",
    "ftp"
]


class CloudAccessToken:
    """Class used to specify cloud access information for outputting to a cloud service."""

    def __init__(self, service: str):
        """This constructor is not meant for direct use, use one of the subclasses instead."""
        self._service = service

    @property
    def service(self) -> str:
        """Which cloud service is being used.

        Returns:
            str: service
        """
        return self._service

    @service.setter
    def service(self, value: str):
        """Setter for service

        Args:
            value (str): cloud service to use

        Raises:
            ValueError: value does not correspond to a known/supported service
        """
        if not self.is_valid_service(value):
            raise ValueError(f'Unsupported cloud service "{value}".')
        self._service = value

    @property
    @abstractmethod
    def as_dict(self) -> dict:
        """The cloud access token as a dict, for building the json.

        Raises:
            NotImplementedError: all subclasses override this method

        Returns:
            dict: dict representation of this cloud access token
        """
        pass

    @property
    def json(self) -> str:
        """The cloud access token as AOP-compatible json data.

        Returns:
            str: json string
        """
        return json.dumps(self.as_dict)

    @staticmethod
    def is_valid_service(value: str) -> bool:
        """Check if the given value is a valid service string.

        Args:
            value (str): the service to check

        Returns:
            bool: whether value is valid
        """
        return value in SERVICES

    @staticmethod
    def list_available_services() -> List[str]:
        """List all available services.

        Returns:
            List[str]: list of available service strings
        """
        return SERVICES

    @staticmethod
    def from_OAuth(service: str, token: str) -> 'OAuthToken':
        """Create a token from an OAuth string and service name.

        Args:
            service (str): cloud service
            token (str): OAuth access token

        Returns:
            OAuthToken: created token
        """
        return OAuthToken(service, token)

    @staticmethod
    def from_AWS(key_id: str, secret_key: str):
        """Create a token from Amazon S3 access key id and secret access key.

        Args:
            key_id (str): AWS access key ID
            secret_key (str): AWS secret access key

        Returns:
            AWSToken: created token
        """
        return AWSToken(key_id, secret_key)

    @staticmethod
    def from_FTP(host: str, port: int = None, user: str = None, password: str = None) -> 'FTPToken':
        """Create a token from FTP info

        When an argument is / defaults to None, no data about it is sent to the AOP server.
        The AOP server will then fill in default values.

        Args:
            host (str): host name or IP address
            port (int, optional): port to use. Defaults to None.
            user (str, optional): user name. Defaults to None.
            password (str, optional): password for user. Defaults to None.

        Returns:
            FTPToken: created token
        """
        return FTPToken(host, False, port, user, password)

    @staticmethod
    def from_SFTP(host: str, port: int = None, user: str = None, password: str = None) -> 'FTPToken':
        """Create a token from SFTP info

        When an argument is / defaults to None, no data about it is sent to the AOP server.
        The AOP server will then fill in default values.

        Args:
            host (str): host name or IP address
            port (int, optional): port to use. Defaults to None.
            user (str, optional): user name. Defaults to None.
            password (str, optional): password for user. Defaults to None.

        Returns:
            FTPToken: created token
                      This is an FTPToken object, with sftp=True passed into the constructor.
                      The only difference with FTP is CloudAccessToken.servicename.
        """
        return FTPToken(host, True, port, user, password)


class OAuthToken(CloudAccessToken):
    """Inherits from CloudAccessToken, to be used for OAuth tokens"""

    def __init__(self, service: str, token: str):
        """Constructor for OAuthToken

        Args:
            service (str): service to use (e.g. Dropbox)
            token (str): OAuth token
        """
        super().__init__(service)
        self._token = token

    @property
    def token(self) -> str:
        """The OAuth token as a string.

        Returns:
            str: OAuth token
        """
        return self._token

    @property
    def as_dict(self):
        """Override the CloudAccessToken method."""
        return {
            "output_location": self.service,
            "cloud_access_token": self.token
        }


class AWSToken(CloudAccessToken):
    """Inherits from CloudAccessToken, to be used for AWS tokens"""

    def __init__(self, key_id: str, secret_key: str):
        super().__init__("aws_s3")
        self._key_id = key_id
        self._secret_key = secret_key

    @property
    def key_id(self) -> str:
        """AWS access key ID

        Returns:
            str: key ID
        """
        return self._key_id

    @property
    def secret_key(self) -> str:
        """AWS secret key

        Returns:
            str: secret key
        """
        return self._secret_key

    @property
    def as_dict(self):
        """Override the CloudAccessToken method."""
        return {
            "output_location": self.service,
            "cloud_access_token": {
                "access_key": self.key_id,
                "secret_access_key": self.secret_key
            }
        }


class FTPToken(CloudAccessToken):
    """Inherits from CloudAccessToken, to be used for FTP/SFTP tokens"""

    def __init__(self, host: str, sftp: bool = False, port: int = None, user: str = None, password: str = None):
        """Constructor for FTPToken

        This class is used for both FTP and SFTP.

        Args:
            host (str): host name or IP address
            sftp (bool, optional): whether to use SFTP (else FTP). Defaults to False.
            port (int, optional): port number. Defaults to None.
            user (str, optional): user name for the FTP/SFTP server. Defaults to None.
            password (str, optional): password for the FTP/SFTP. Defaults to None.
        """
        super().__init__("sftp" if sftp else "ftp")
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    @property
    def host(self) -> str:
        """host name or IP address

        Returns:
            str: host name or IP address
        """
        return self._host

    @property
    def port(self) -> str:
        """port number

        Returns:
            str: port number
        """
        return self._port

    @property
    def user(self) -> str:
        """user name

        Returns:
            str: user name
        """
        return self._user

    @property
    def password(self) -> str:
        """password

        Returns:
            str: password
        """
        return self._password

    @property
    def as_dict(self):
        """Override the CloudAccessToken method."""
        cloud_access_token = {
            "host": self.host
        }
        if self.port is not None:
            cloud_access_token["port"] = self.port
        if self.user is not None:
            cloud_access_token["user"] = self.user
        if self.password is not None:
            cloud_access_token["password"] = self.password

        return {
            "output_location": self.service,
            "cloud_access_token": cloud_access_token
        }


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
        if not (value == "raw" or value == "base64"):
            raise ValueError(
                f'Encoding must be either "raw" or "base64", was "{value}".')
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
        self._converter = value

    @property
    def cloud_access_token(self) -> 'CloudAccessToken':
        """Access token used to access various cloud services for output storage.

        It should be an instance of `CloudAccessToken`.

        Returns:
            CloudAccessToken: access token
        """
        return self._cloud_access_token

    @cloud_access_token.setter
    def cloud_access_token(self, value: 'CloudAccessToken'):
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
        self._server_directory = value

    @property
    def pdf_options(self) -> 'PDFOptions':
        """Optional PDF options.

        Should be an instance of `PDFOptions`

        Returns:
            PDFOptions: PDF options
        """
        return self._pdf_options

    @pdf_options.setter
    def pdf_options(self, value: 'PDFOptions'):
        self._pdf_options = value


class PDFOptions:
    """Class of optional PDF options.

    The properties of this class define all possible PDF output options.
    All of them are optional, which is why passing an instance of this class in an OutputConfig is also optional.

    The getters for the properties return the value the server uses as default value if the value is set to None.
    These default values are not passed to the json or dict representation of the object and thus not explicitly sent to the AOP server.
    """

    _even_page = None
    _merge_making_even = None
    _read_password = None
    _modify_password = None
    _password_protection_flag = None
    _watermark = None
    _lock_form = None
    _copies = None
    _page_margin = None
    _landscape = False
    _page_width = None
    _page_height = None
    _page_format = None
    _merge = None

    def __str__(self):
        return self.json

    @property
    def json(self) -> str:
        """Get the json representation of these PDF options.

        The json representation is a direct json dump of the dict representation.
        The dict representation is accessed through the as_dict property.

        Returns:
            str: json string
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """Get the dict representation of these PDF options.

        Returns:
            dict: options as dict
        """
        result = {}
        if self._even_page is not None:
            result["output_even_page"] = self._even_page
        if self._merge_making_even is not None:
            result["output_merge_making_even"] = self._merge_making_even
        if self._modify_password is not None:
            result["output_modify_password"] = self._modify_password
        if self._read_password is not None:
            result["output_read_password"] = self._read_password
        if self._password_protection_flag is not None:
            result["output_password_protection_flag"] = self._password_protection_flag
        if self._watermark is not None:
            result["output_watermark"] = self._watermark
        if self._lock_form is not None:
            result["lock_form"] = self._lock_form
        if self._copies is not None:
            result["output_copies"] = self._copies
        if self.page_margin is not None:
            if isinstance(self._page_margin, dict):
                for pos, value in self._page_margin.items():
                    result[f"output_page_margin_{pos}"] = value
            else:
                result["output_page_margin"] = self._page_margin
        if self._page_width is not None:
            result["output_page_width"] = self._page_width
        if self._page_height is not None:
            result["output_page_height"] = self._page_height
        if self._page_format is not None:
            result["output_page_format"] = self._page_format
        if self._merge is not None:
            result["output_merge"] = self._merge

    @property
    def even_page(self) -> bool:
        """If you want your output to have even pages, for example printing on both sides after merging, you can set this to be true.

        Returns:
            bool: even_page
        """
        return False if self._even_page is None else self._even_page

    @even_page.setter
    def even_page(self, value: bool):
        # set to None instead of False to omit from the json
        self._even_page = True if value else None

    @property
    def merge_making_even(self) -> bool:
        """Merge each given document making even paged.

        Returns:
            bool: merge_making_even
        """
        return False if self._merge_making_even is None else self._merge_making_even

    @merge_making_even.setter
    def merge_making_even(self, value: bool):
        self._merge_making_even = True if value else None

    @property
    def read_password(self) -> str:
        """The password needed to open the PDF.

        Returns:
            str: read_password
        """
        return self._read_password

    @read_password.setter
    def read_password(self, value: str):
        self._read_password = value

    @property
    def modify_password(self) -> str:
        """The password needed to modify the PDF.

        Returns:
            str: modify_password
        """
        return self.read_password if self._modify_password is None else self._modify_password

    @modify_password.setter
    def modify_password(self, value: str):
        self._modify_password = value

    @property
    def password_protection_flag(self) -> int:
        """Bit field explained in the PDF specs in table 3.20 in section 3.5.2, should be given as an integer.

        [More info.](https://pdfhummus.com/post/147451287581/hummus-1058-and-pdf-writer-updates-encryption)

        Returns:
            int: password_protection_flag
        """
        return 4 if self._password_protection_flag is None else self._password_protection_flag

    @password_protection_flag.setter
    def password_protection_flag(self, value: int):
        self._password_protection_flag = int(value)

    @property
    def watermark(self) -> str:
        """Setting this generates a diagonal custom watermark on every page in the PDF file

        Returns:
            str: watermark
        """
        return self._watermark

    @watermark.setter
    def watermark(self, value: str):
        self._watermark = value

    @property
    def lock_form(self) -> bool:
        """Locks / flattens the forms in the PDF.

        Returns:
            bool: lock_form
        """
        return False if self._lock_form is None else self._lock_form

    @lock_form.setter
    def lock_form(self, value: bool):
        self._lock_form = True if value else None

    @property
    def copies(self) -> int:
        """Repeats the output pdf for the given number of times.

        Returns:
            int: copies
        """
        return self._copies

    @copies.setter
    def copies(self, value: int):
        self._copies = int(value)

    @property
    def page_margin(self) -> Union[int, dict]:
        """Margin in px.

        Returns either a dict containing:
        ```python
        {
            "top": int,
            "bottom": int,
            "left": int,
            "right": int
        }
        ```
        or just an int to be used on all sides.

        Returns:
            Union[int, dict]: page_margin
        """
        return self._page_margin

    def set_page_margin_at(self, value: int, position: str = None):
        """Set page_margin

        Either set the position for all margin positions (if position is None) or set a specific one.
        The setter for the page_margin property sets the margin for all positions.

        Args:
            value (int): page margin
            position (str, optional): "top", "bottom", "left" or "right". Defaults to None.
        """
        if position is not None:
            if isinstance(self._page_margin, dict):
                # page margin is already a dict, add/change this position
                self._page_margin[position] = value
            elif self._page_margin is None:
                # page margin not yet defined, set it to a dict with this position defined
                self._page_margin = {
                    position: value
                }
            else:
                # page margin defined but no dict, convert to dict first
                current = self._page_margin
                self._page_margin = {
                    "top": current,
                    "bottom": current,
                    "left": current,
                    "right": current
                }
                self._page_margin[position] = value
        else:
            self._page_margin = value

    @page_margin.setter
    def page_margin(self, value: int):
        self.set_page_margin_at(value, position=None)

    @property
    def page_orientation(self) -> str:
        """The page orientation, portrait or landscape.

        Returns:
            str: page_orientation
        """
        return "landscape" if self._landscape else "portrait"

    @page_orientation.setter
    def page_orientation(self, value: str):
        self._landscape = True if value == "landscape" else False

    @property
    def page_width(self) -> Union[str, int]:
        """Page width in px, mm, cm, in. No unit means px.

        Returns:
            Union[str, int]: page_width
        """
        return self._page_width

    @page_width.setter
    def page_width(self, value: Union[str, int]):
        self._page_width = value

    @property
    def page_height(self):
        """Page height in px, mm, cm, in. No unit means px.

        Returns:
            Union[str, int]: page_height
        """
        return self._page_height

    @page_height.setter
    def page_height(self, value: Union[str, int]):
        self._page_height = value

    @property
    def page_format(self) -> str:
        """The page format: "a4" (default) or "letter"

        Returns:
            str: page_format
        """
        return "a4" if self._page_format is None else self._page_format

    @page_format.setter
    def page_format(self, value: str):
        self._page_format = value

    @property
    def merge(self) -> bool:
        """If True: instead of returning back a zip file for multiple output, merge it.

        Returns:
            bool: merge
        """
        return False if self._merge is None else self._merge

    @merge.setter
    def merge(self, value: bool):

        self._merge = value


class ServerConfig:
    """This config class is used to specify the AOP server to interact with."""

    def __init__(self, server_url: str, api_key: str = None):
        """Constructor for ServerConfig

        Args:
            server_url (str): URL to contact the server at
            api_key (str, optional): api key to use for the application
        """
        self._api_key = api_key
        self.server_url = server_url

    @property
    def api_key(self) -> str:
        """The API key to be used for the application.

        Returns:
            str: api key
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = value

    @property
    def server_url(self) -> str:
        """URL at which to contact the server.

        Returns:
            str: server URL
        """
        return self._server_url

    @server_url.setter
    def server_url(self, value: str):
        if (urlparse(value).scheme == ''):
            self._server_url = "http://" + value
            logging.warning(
                f'No scheme found in "{value}", assuming "{self._server_url}".')
        else:
            self._server_url = value

    def is_reachable(self) -> bool:
        """Contact the server to see if it is reachable.

        Returns:
            bool: whether the server at server_url is reachable
        """
        try:
            r = requests.get(urljoin(self.server_url, "marco"))
            return r.text == "polo"
        except requests.exceptions.ConnectionError:
            return False
