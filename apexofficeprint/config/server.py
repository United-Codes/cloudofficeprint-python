import logging
import requests
from urllib.parse import urljoin, urlparse

class ServerConfig:
    def __init__(self, api_key: str = None):
        self.api_key: str = api_key
        """API key to use for the application."""

    @property
    def as_dict(self):
        result = {}

        if self.api_key:
            result["api_key"] = self.api_key

        return result


class Server:
    """This config class is used to specify the AOP server to interact with."""

    # TODO: proxies

    # TODO: "logging", "ipp", "post_process", "conversion", "merge"

    # TODO: get_version(), ... (there are some server statuses on other paths than /marco)

    def __init__(self, url: str, config: ServerConfig = None):
        """
        Args:
            url (str): `Server.url`.
            config (ServerConfig): `Server.config`
        """
        self.url = url
        self.config: ServerConfig = config
        """# TODO"""

    @property
    def url(self) -> str:
        """URL at which to contact the server."""
        return self._url

    @url.setter
    def url(self, value: str):
        if (urlparse(value).scheme == ''):
            self._url = "http://" + value
            logging.warning(
                f'No scheme found in "{value}", assuming "{self._url}".')
        else:
            self._url = value

    def is_reachable(self) -> bool:
        """Contact the server to see if it is reachable.

        Returns:
            bool: whether the server at `Server.url` is reachable
        """
        try:
            r = requests.get(urljoin(self.url, "marco"))
            return r.text == "polo"
        except requests.exceptions.ConnectionError:
            return False

    def _raise_if_unreachable(self):
        if not self.is_reachable():
            raise ConnectionError(
                f"Could not reach server at {self.url}")
