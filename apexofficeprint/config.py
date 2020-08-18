"""
Module for output configurations.

The classes under this module encapsulate various configuration options for a print job.
They are to be used with `job.PrintJob`.
"""

from typing import List, Union
from abc import abstractmethod, ABC
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


class CloudAccessToken(ABC):
    """Abstract base class for classes used to specify cloud access information for outputting to a cloud service."""

    def __init__(self, service: str):
        self._service = service

    @property
    def service(self) -> str:
        """Which cloud service is being used."""
        return self._service

    @service.setter
    def service(self, value: str):
        if not self.is_valid_service(value):
            raise ValueError(f'Unsupported cloud service "{value}".')
        self._service = value

    @property
    @abstractmethod
    def as_dict(self) -> dict:
        """The cloud access token as a dict, for building the json."""
        pass

    @property
    def json(self) -> str:
        """The cloud access token as AOP-compatible json data."""
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
    """`CloudAccessToken` to be used for OAuth tokens"""

    def __init__(self, service: str, token: str):
        """
        Args:
            service (str): service to use (e.g. Dropbox)
            token (str): OAuth token
        """
        super().__init__(service)
        self.token: str = token
        """OAuth token"""

    @property
    def as_dict(self):
        return {
            "output_location": self.service,
            "cloud_access_token": self.token
        }


class AWSToken(CloudAccessToken):
    """`CloudAccessToken` to be used for AWS tokens"""

    def __init__(self, key_id: str, secret_key: str):
        """
        Args:
            key_id (str): AWS access key ID
            secret_key (str): AWS secret key
        """
        super().__init__("aws_s3")
        self.key_id: str = key_id
        """AWS access key ID"""
        self.secret_key: str = secret_key
        """AWS secret key"""

    @property
    def as_dict(self):
        return {
            "output_location": self.service,
            "cloud_access_token": {
                "access_key": self.key_id,
                "secret_access_key": self.secret_key
            }
        }


class FTPToken(CloudAccessToken):
    """`CloudAccessToken` to be used for FTP/SFTP tokens"""

    def __init__(self, host: str, sftp: bool = False, port: int = None, user: str = None, password: str = None):
        """
        Args:
            host (str): host name or IP address
            sftp (bool, optional): whether to use SFTP (else FTP). Defaults to False.
            port (int, optional): port number. Defaults to None.
            user (str, optional): user name for the FTP/SFTP server. Defaults to None.
            password (str, optional): password for the FTP/SFTP server. Defaults to None.
        """
        super().__init__("sftp" if sftp else "ftp")
        self.host: str = host
        """Host name or IP address of the FTP/SFTP server."""
        self.port: int = port
        """Port number of the FTP/SFTP server."""
        self.user: str = user
        """User name for the FTP/SFTP server."""
        self.password: str = password
        """Password for `FTPToken.user`."""

    @property
    def as_dict(self):
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
        """
        Args:
            filetype (str, optional): File type (as extension). Defaults to None.
            encoding (str, optional): Encoding. Defaults to "raw".
            converter (str, optional): Converter. Defaults to "libreoffice".
            cloud_access_token (CloudAccessToken, optional): Cloud access token. Defaults to None.
            server_directory (str, optional): Server directory. Defaults to None.
            pdf_options (PDFOptions, optional): PDF options. Defaults to None.
        """
        self.filetype: str = filetype
        """The file type (as extension) to use for the output."""
        self.converter: str = converter
        """The pdf converter to use.

        Can be "libreoffice", "officetopdf" or any custom defined converter.
        Custom converters are configurated in the AOP server's `aop_config.json` file.
        """
        self._cloud_access_token: CloudAccessToken = cloud_access_token
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
        if self._cloud_access_token is not None:
            result.update(self._cloud_access_token.as_dict)
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


class PDFOptions:
    """Class of optional PDF options.

    The properties of this class define all possible PDF output options.
    All of them are optional, which is why passing an instance of this class in an OutputConfig is also optional.

    The getters for the properties return the value the server uses as default value if the value is set to None.
    These default values are not passed to the json or dict representation of the object and thus not explicitly sent to the AOP server.
    """

    read_password: str = None
    """The password needed to open the PDF."""
    watermark: str = None
    """Setting this generates a diagonal custom watermark on every page in the PDF file"""
    page_width: Union[str, int] = None
    """Page width in px, mm, cm, in. No unit means px."""
    page_height: Union[str, int] = None
    """Page height in px, mm, cm, in. No unit means px."""

    _even_page = None
    _merge_making_even = None
    _modify_password = None
    _password_protection_flag = None
    _lock_form = None
    _copies = None
    _page_margin = None
    _landscape = False
    _page_format = None
    _merge = None

    def __str__(self):
        return self.json

    @property
    def json(self) -> str:
        """The json representation of these PDF options.

        The json representation is a direct json dump of the dict representation.
        The dict representation is accessed through the `as_dict` property.
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """The dict representation of these PDF options."""
        result = {}
        if self._even_page is not None:
            result["output_even_page"] = self._even_page
        if self._merge_making_even is not None:
            result["output_merge_making_even"] = self._merge_making_even
        if self._modify_password is not None:
            result["output_modify_password"] = self._modify_password
        if self.read_password is not None:
            result["output_read_password"] = self.read_password
        if self._password_protection_flag is not None:
            result["output_password_protection_flag"] = self._password_protection_flag
        if self.watermark is not None:
            result["output_watermark"] = self.watermark
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
        if self.page_width is not None:
            result["output_page_width"] = self.page_width
        if self.page_height is not None:
            result["output_page_height"] = self.page_height
        if self._page_format is not None:
            result["output_page_format"] = self._page_format
        if self._merge is not None:
            result["output_merge"] = self._merge

    @property
    def even_page(self) -> bool:
        """If you want your output to have even pages, for example printing on both sides after merging, you can set this to be true."""
        return False if self._even_page is None else self._even_page

    @even_page.setter
    def even_page(self, value: bool):
        # set to None instead of False to omit from the json
        self._even_page = True if value else None

    @property
    def merge_making_even(self) -> bool:
        """Merge each given document making even paged."""
        return False if self._merge_making_even is None else self._merge_making_even

    @merge_making_even.setter
    def merge_making_even(self, value: bool):
        self._merge_making_even = True if value else None

    @property
    def modify_password(self) -> str:
        """The password needed to modify the PDF."""
        return self.read_password if self._modify_password is None else self._modify_password

    @modify_password.setter
    def modify_password(self, value: str):
        self._modify_password = value

    @property
    def password_protection_flag(self) -> int:
        """Bit field explained in the PDF specs in table 3.20 in section 3.5.2, should be given as an integer.

        [More info.](https://pdfhummus.com/post/147451287581/hummus-1058-and-pdf-writer-updates-encryption)
        """
        return 4 if self._password_protection_flag is None else self._password_protection_flag

    @password_protection_flag.setter
    def password_protection_flag(self, value: int):
        self._password_protection_flag = int(value)

    @property
    def lock_form(self) -> bool:
        """Locks / flattens the forms in the PDF."""
        return False if self._lock_form is None else self._lock_form

    @lock_form.setter
    def lock_form(self, value: bool):
        self._lock_form = True if value else None

    @property
    def copies(self) -> int:
        """Repeats the output pdf for the given number of times."""
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
        or just an int to be used on all sides."""
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
        """The page orientation, portrait or landscape."""
        return "landscape" if self._landscape else "portrait"

    @page_orientation.setter
    def page_orientation(self, value: str):
        self._landscape = True if value == "landscape" else False

    @property
    def page_format(self) -> str:
        """The page format: "a4" (default) or "letter"."""
        return "a4" if self._page_format is None else self._page_format

    @page_format.setter
    def page_format(self, value: str):
        self._page_format = value

    @property
    def merge(self) -> bool:
        """If True: instead of returning back a zip file for multiple output, merge it."""
        return False if self._merge is None else self._merge

    @merge.setter
    def merge(self, value: bool):
        self._merge = value


class ServerConfig:
    """This config class is used to specify the AOP server to interact with."""

    def __init__(self, server_url: str, api_key: str = None):
        """
        Args:
            server_url (str): URL to contact the server at.
            api_key (str, optional): API key to use for the application.
        """
        self.api_key: str = api_key
        """API key to use for the application."""
        self.server_url = server_url

    @property
    def server_url(self) -> str:
        """URL at which to contact the server."""
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
