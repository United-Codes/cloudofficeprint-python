from typing import List
from abc import abstractmethod
import json

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
