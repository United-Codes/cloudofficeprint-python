"""
Module containing the PrintJob class, which is also exposed at package level.
"""

import requests
import json
from .config import OutputConfig, ServerConfig
from .exceptions import AOPError
from .response import Response
from .resource import Resource
from .elements import Element
from typing import Union, List, Dict

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
                 data: Union[Element, Dict[str, Element]],
                 server_config: ServerConfig,
                 output_config: OutputConfig = None):
        """
        Args:
            template (apexofficeprint.resource.Resource): `PrintJob.template`.
            data (Union[Element, Dict[str, Element]]): `PrintJob.data`.
            server_config (apexofficeprint.config.ServerConfig): `PrintJob.server_config`.
            output_config (apexofficeprint.config.OutputConfig, optional): `Printjob.output_config`. Defaults to `apexofficeprint.config.ServerConfig`().
        """
        self.data: Union[List[Element], Element] = data
        """ # TODO """
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

        # TODO: prepend / append files
        # TODO: support REST endpoint as file source (see docs)

        if isinstance(self.data, dict):
            result["files"] = [{
                "filename": name,
                "data": data.as_dict
            } for name, data in self.data.items()]
        else:
            result["files"] = [{"data": self.data.as_dict}]

        return result
