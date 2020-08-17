"""
Module containing the PrintJob class, which is also exposed at package level.
"""

import requests
import json
from .config import OutputConfig, ServerConfig
from .exceptions import AOPError
from .response import Response
from .resource import Resource
from typing import Union

STATIC_OPTS = {
    "tool": "python"
    # "version": "18.2" # optional
}


class PrintJob:
    """A print job for a AOP server.

    This class contains all configuration options, resources, render elements ...
    and the `PrintJob.execute` method to combine all these and send a request to the AOP server.
    """

    def __init__(self,
                 template: Resource,
                 server_config: ServerConfig,
                 output_config: OutputConfig = None):
        self._server_config = server_config
        self._output_config = output_config if output_config else OutputConfig()
        self._template = template

    def execute(self) -> Union[Response, AOPError]:
        """# TODO: document (auto generate args etc.) when finished
        """
        if not self.server_config.is_reachable():
            raise ConnectionError(
                f"Could not reach server at {self.server_config.server_url}")

        res = requests.post(self.server_config.server_url, json=self.as_dict)

        if res.status_code != 200:
            raise AOPError(res.text)
        else:
            return Response(res)

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
        (`PrintJob.json`).

        Returns:
            dict: dict representation of this print job
        """
        result = STATIC_OPTS

        if self.server_config.api_key is not None:
            result["api_key"] = self.server_config.api_key

        result["output"] = self.output_config.as_dict

        result["template"] = self.template.template_dict

        # TODO: this is test data, should be handled with render elements
        result["files"] = [
            json.loads('{"data":{"testVar": "HELLO!"}}')
        ]
        return result

    @property
    def server_config(self) -> ServerConfig:
        """Server configuration to be used for this print job.

        Should be an instance of `ServerConfig`

        Returns:
            ServerConfig: server configuration
        """
        return self._server_config

    @server_config.setter
    def server_config(self, value: ServerConfig):
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
        self._output_config = value

    @property
    def template(self) -> Resource:
        """Template to use for this print job.

        Should be an instance of `Resource`

        Returns:
            Resource: resource to use as template
        """
        return self._template

    @template.setter
    def template(self, resource: Resource):
        self._template = resource
