"""
Module containing the PrintJob class, which is also exposed at package level.
"""

import requests
import asyncio
import json
from .config import OutputConfig, Server
from .exceptions import AOPError
from .response import Response
from .resource import Resource
from .elements import Element
from typing import Union, List, Dict
from functools import partial

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
                 server: Server,
                 output_config: OutputConfig = None):
        """
        Args:
            template (apexofficeprint.resource.Resource): `PrintJob.template`.
            data (Union[Element, Dict[str, Element]]): `PrintJob.data`.
            server (apexofficeprint.config.Server): `PrintJob.server`.
            output_config (apexofficeprint.config.OutputConfig, optional): `Printjob.output_config`. Defaults to `apexofficeprint.config.ServerConfig`().
        """
        self.data: Union[List[Element], Element] = data
        """ # TODO """
        self.server: Server = server
        """Server to be used for this print job."""
        self.output_config: OutputConfig = output_config if output_config else OutputConfig()
        """Output configuration to be used for this print job."""
        self.template: Resource = template
        """Template to use for this print job."""

    def execute(self) -> Union[Response, AOPError]:
        """# TODO: document (auto generate args etc.) when finished
        """
        self.server._raise_if_unreachable()
        return self._handle_response(requests.post(self.server.url, json=self.as_dict))

    async def execute_async(self) -> Union[Response, AOPError]:
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(requests.post, self.server.url, json=self.as_dict)
            )
        )

    @staticmethod
    def execute_full_json(json_data: str, server: Server):
        server._raise_if_unreachable()
        return PrintJob._handle_response(requests.post(server.url, data=json_data, headers={"Content-type": "application/json"}))

    @staticmethod
    async def execute_full_json_async(json_data: str, server: Server):
        server._raise_if_unreachable()
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(requests.post, server.url, data=json_data, headers={"Content-type": "application/json"})
            )
        )

    @staticmethod
    def _handle_response(res: requests.Response):
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

        if self.server.config:
            result.update(self.server.config.as_dict)

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
