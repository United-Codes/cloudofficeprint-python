import json
from typing import List
from abc import ABC, abstractmethod

__all__ = [
    "CloudAccessToken",
    "OAuthToken",
    "AWSToken",
    "FTPToken"
]

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
            service (str): `CloudAccessToken.service`
            token (str): `OAuthToken.token`
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
            key_id (str): `AWSToken.key_id`
            secret_key (str): `AWSToken.secret_key`
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
            host (str): `FTPToken.host`
            sftp (bool, optional): whether to use SFTP (else FTP). Defaults to False.
            port (int, optional): `FTPToken.port`. Defaults to None.
            user (str, optional): `FTPToken.user`. Defaults to None.
            password (str, optional): `FTPToken.password`. Defaults to None.
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
