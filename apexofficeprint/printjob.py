import json
from .aop_config import ServerConfig, OutputConfig

STATIC_OPTS = {
    "tool": "python",
    "version": "18.2"
}


class PrintJob:
    def __init__(self,
                 server_config: ServerConfig,
                 output_config: OutputConfig):
        self._server_config = server_config
        self._output_config = output_config

    @property
    def json(self) -> str:
        return json.dumps(self.as_dict)
    
    @property
    def as_dict(self) -> dict:
        result = STATIC_OPTS

        if self.server_config.api_key is not None:
            result["api_key"] = self.server_config.api_key

        result["output"] = self.output_config.as_dict

        # add more stuff to result here

        return result

    # TODO: docstrings
    @property
    def server_config(self):
        return self._server_config

    @server_config.setter
    def server_config(self, value: ServerConfig):
        self._server_config = value

    @property
    def output_config(self):
        return self._output_config

    @output_config.setter
    def output_config(self, value: OutputConfig):
        self._output_config = value
