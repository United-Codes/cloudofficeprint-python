class ServerConfig:
    def __init__(self, api_key: str, server_url: str):
        """Constructor for ServerConfig

        Args:
            api_key (str): api key to use for the application
            server_url (str): URL to contact the server at
        """
        self._api_key = api_key
        self._server_url = server_url

    @property
    def api_key(self) -> str:
        """The API key to be used for the application.

        Returns:
            str: api key
        """
        return self._api_key

    @property
    def server_url(self) -> str:
        """URL at which to contact the server.

        Returns:
            str: server url
        """
        return self._server_url
