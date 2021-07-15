"""
Module containing the PrintJob class, which is also exposed at package level.
"""

from apexofficeprint.elements.rest_source import RESTSource
import requests
import asyncio
import json
from .config import OutputConfig, Server
from .exceptions import AOPError
from .response import Response
from .resource import Resource
from .elements import Element, ElementCollection
from typing import Union, List, Dict, Mapping
from functools import partial

STATIC_OPTS = {
    "tool": "python",
    # "version": "18.2", # optional: version of AOP JSON format
    "python_sdk_version": "21.1",
}


class PrintJob:
    """A print job for a AOP server.

    This class contains all configuration options, resources, render elements ...
    and the `PrintJob.execute` method to combine all these and send a request to the AOP server.
    """

    def __init__(self,
                 template: Resource,
                 data: Union[Element, Mapping[str, Element], RESTSource],
                 server: Server,
                 output_config: OutputConfig = None,
                 subtemplates: Dict[str, Resource] = {},
                 prepend_files: List[Resource] = [],
                 append_files: List[Resource] = []):
        """
        Args:
            template (Resource): `PrintJob.template`.
            data (Union[Element, Mapping[str, Element]], RESTSource): `PrintJob.data`.
            server (Server): `PrintJob.server`.
            output_config (OutputConfig, optional): `Printjob.output_config`. Defaults to `OutputConfig`().
            subtemplates (Dict[str, Resource]): `Printjob.subtemplates`. Defaults to {}.
            prepend_files (List[Resource]): `Printjob.prepend_files`. Defaults to [].
            append_files (List[Resource]): `Printjob.append_files`. Defaults to [].
        """
        self.data: Union[Element, Mapping[str, Element], RESTSource] = data
        """This is either:
        - An `Element` (e.g. an `ElementCollection`)
        - A mapping, containing file names as keys and an `Element` as data. Multiple files will be produced from the different datas, the result is a zip file containing them.
        In the first case, no output file name is specified and the server will name it "file0".
        """
        self.server: Server = server
        """Server to be used for this print job."""
        self.output_config: OutputConfig = output_config if output_config else OutputConfig()
        """Output configuration to be used for this print job."""
        self.template: Resource = template
        """Template to use for this print job."""
        self.subtemplates: Dict[str, Resource] = subtemplates
        """Subtemplates for this print job, accessible (in docx) through `{?include subtemplate_dict_key}`"""
        self.prepend_files: List[Resource] = prepend_files
        """Files to prepend to the output file."""
        self.append_files: List[Resource] = append_files
        """Files to append to the output file."""

    def execute(self) -> Response:
        """Execute this print job."""
        self.server._raise_if_unreachable()
        return self._handle_response(requests.post(self.server.url, proxies=self.server.config.proxies if self.server.config is not None else None, json=self.as_dict))

    async def execute_async(self) -> Response:
        """Async version of `PrintJob.execute`"""
        self.server._raise_if_unreachable()
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(
                    requests.post,
                    self.server.url,
                    proxies=self.server.config.proxies if self.server.config is not None else None,
                    json=self.as_dict
                )
            )
        )

    @staticmethod
    def execute_full_json(json_data: str, server: Server) -> Response:
        server._raise_if_unreachable()
        return PrintJob._handle_response(requests.post(server.url, proxies=server.config.proxies if server.config is not None else None, data=json_data, headers={"Content-type": "application/json"}))

    @staticmethod
    async def execute_full_json_async(json_data: str, server: Server) -> Response:
        server._raise_if_unreachable()
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(
                    requests.post,
                    server.url,
                    proxies=server.config.proxies if server.config is not None else None,
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
        result = dict(STATIC_OPTS) # Copy of STATIC_OPTS! Otherwise everything we add to 'result' will also be added to 'STATIC_OPTS'
        # server config goes in the upper level
        if self.server.config:
            result.update(self.server.config.as_dict)

        # output config goes in "output"
        # and decides where its sub-configs go through its as_dict property
        # (e.g. PDFConfigs are just appended at this "output" level)
        result["output"] = self.output_config.as_dict

        result["template"] = self.template.template_dict

        # If output_type is not specified, set this to the template filetype
        if 'output_type' not in self.output_config.as_dict.keys():
            result['output']['output_type'] = result['template']['template_type']

        if isinstance(self.data, Mapping):
            result["files"] = [{
                "filename": name,
                "data": data.as_dict
            } for name, data in self.data.items()]
        elif isinstance(self.data, RESTSource):
            result['files'] = [self.data.as_dict]
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
