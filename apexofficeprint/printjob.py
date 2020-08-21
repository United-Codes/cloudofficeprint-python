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
from typing import Union, List, Dict, Mapping
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
                 data: Union[Element, Mapping[str, Element]],
                 server: Server,
                 output_config: OutputConfig = None):
        """
        Args:
            template (apexofficeprint.resource.Resource): `PrintJob.template`.
            data (Union[Element, Mapping[str, Element]]): `PrintJob.data`.
            server (apexofficeprint.config.Server): `PrintJob.server`.
            output_config (apexofficeprint.config.OutputConfig, optional): `Printjob.output_config`. Defaults to `apexofficeprint.config.ServerConfig`().
        """
        self.data: Union[Element, Mapping[str, Element]] = data
        """ # TODO """
        self.server: Server = server
        """Server to be used for this print job."""
        self.output_config: OutputConfig = output_config if output_config else OutputConfig()
        """Output configuration to be used for this print job."""
        self.template: Resource = template
        """Template to use for this print job."""
        self.subtemplates: Dict[str, Resource] = {}
        """Subtemplates for this print job, accessible (in docx) through `{?include subtemplate_dict_key}`"""
        self.append_files: List[Resource] = []
        self.prepend_files: List[Resource] = []

    def execute(self) -> Response:
        """# TODO: document
        """
        self.server._raise_if_unreachable()
        return self._handle_response(requests.post(self.server.url, json=self.as_dict))

    async def execute_async(self) -> Response:
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(
                    requests.post,
                    self.server.url,
                    json=self.as_dict
                )
            )
        )

    @staticmethod
    def execute_full_json(json_data: str, server: Server) -> Response:
        server._raise_if_unreachable()
        return PrintJob._handle_response(requests.post(server.url, data=json_data, headers={"Content-type": "application/json"}))

    @staticmethod
    async def execute_full_json_async(json_data: str, server: Server) -> Response:
        server._raise_if_unreachable()
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(
                    requests.post,
                    server.url,
                    data=json_data,
                    headers={"Content-type": "application/json"}
                )
            )
        )

    @staticmethod
    def _handle_response(res: requests.Response) -> Response:
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

        # TODO: support REST endpoint as file source (see docs)

        if isinstance(self.data, Mapping):
            result["files"] = [{
                "filename": name,
                "data": data.as_dict
            } for name, data in self.data.items()]
        else:
            result["files"] = [{"data": self.data.as_dict}]

        if len(self.prepend_files) > 0:
            result["prepend_files"] = [
                res.secondary_file_dict for res in self.prepend_files
            ]

        if len(self.append_files) > 0:
            result["append_files"] = [
                res.secondary_file_dict for res in self.append_files
            ]

        if len(self.subtemplates) > 0:
            templates_list = []
            for name, res in self.subtemplates.items():
                to_add = res.secondary_file_dict
                to_add["name"] = name
                templates_list.append(to_add)
            result["templates"] = templates_list

        return result
