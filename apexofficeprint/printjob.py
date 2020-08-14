import json
from .config import ServerConfig, OutputConfig

STATIC_OPTS = {
    "tool": "python",
    "version": "18.2"
}

# TODO: somewhere, this class should check whether its templates are compatible and whether they are in turn compatible with the output file type


class PrintJob:
    def __init__(self,
                 server_config: ServerConfig,
                 output_config: OutputConfig):
        self._server_config = server_config
        self._output_config = output_config

    @property
    def json(self) -> str:
        """json equivalent of the dict representation of this print job.

        Returns:
            str: json representation of this print job
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """dict representation of this print job.

        This representation is isomorphic to the json representation
        to send to the server.

        Returns:
            dict: dict representation of this print job
        """
        result = STATIC_OPTS

        if self.server_config.api_key is not None:
            result["api_key"] = self.server_config.api_key

        result["output"] = self.output_config.as_dict

        # add more stuff to result here

        return result

    @property
    def server_config(self) -> ServerConfig:
        """Server configuration to be used for this print job.

        Should be an instance of apexofficeprint.ServerConfig

        Returns:
            ServerConfig: server configuration
        """
        return self._server_config

    @server_config.setter
    def server_config(self, value: ServerConfig):
        """Set server_config

        Args:
            value (ServerConfig): server_config
        """
        self._server_config = value

    @property
    def output_config(self) -> OutputConfig:
        """Output configuration to be used for this print job.

        Returns:
            OutputConfig: output configuration
        """
        return self._output_config

    @output_config.setter
    def output_config(self, value: OutputConfig):
        """Set output_config

        Args:
            value (OutputConfig): output_config
        """
        self._output_config = value
