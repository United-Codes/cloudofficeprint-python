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
        """
        Args:
            template (apexofficeprint.resource.Resource): Template to use for this print job.
            server_config (apexofficeprint.config.ServerConfig): Server configuration to be used for this print job.
            output_config (apexofficeprint.config.OutputConfig, optional): Output configuration to be used for this print job. Defaults to `apexofficeprint.config.ServerConfig`().
        """
        self.server_config: ServerConfig = server_config
        """Server configuration to be used for this print job."""
        self.output_config: OutputConfig = output_config if output_config else OutputConfig()
        """Output configuration to be used for this print job."""
        self.template: Resource = template
        """Template to use for this print job."""

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
        """json equivalent of the dict representation of this print job."""
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """dict representation of this print job.

        This representation is isomorphic to the json representation
        (`PrintJob.json`)."""
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
