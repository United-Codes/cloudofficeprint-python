import requests
import logging
import re
from urllib.parse import urljoin


class ServerConfig:
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
        """Set api_key

        Args:
            value (str): api key
        """
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
        """Set server_url

        Args:
            value (str): server URL
        """
        if (re.search(r":\/\/", value) is None):
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
