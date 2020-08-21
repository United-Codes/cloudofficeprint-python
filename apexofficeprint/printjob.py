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
from .elements import Element, Object
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
            template (Resource): `PrintJob.template`.
            data (Union[Element, Mapping[str, Element]]): `PrintJob.data`.
            server (Server): `PrintJob.server`.
            output_config (OutputConfig, optional): `Printjob.output_config`. Defaults to `OutputConfig`().
        """
        self.data: Union[Element, Mapping[str, Element]] = data
        """This is either:
        - An `Element` (e.g. an `Object`)
        - A mapping, containing file names as keys and an `Element` as data. Multiple files will be produced from the different datas, the result is a zip file containing them.
        In the first case, no output file name is specified and the server will name it "file0".
        """
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
        """Execute this print job."""
        self.server._raise_if_unreachable()
        return self._handle_response(requests.post(self.server.url, proxies=self.server.proxies, json=self.as_dict))

    async def execute_async(self) -> Response:
        """Async version of `PrintJob.execute`"""
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(
                    requests.post,
                    self.server.url,
                    proxies=self.server.proxies,
                    json=self.as_dict
                )
            )
        )

    @staticmethod
    def execute_full_json(json_data: str, server: Server) -> Response:
        server._raise_if_unreachable()
        return PrintJob._handle_response(requests.post(server.url, proxies=server.proxies, data=json_data, headers={"Content-type": "application/json"}))

    @staticmethod
    async def execute_full_json_async(json_data: str, server: Server) -> Response:
        server._raise_if_unreachable()
        return PrintJob._handle_response(
            await asyncio.get_event_loop().run_in_executor(
                None, partial(
                    requests.post,
                    server.url,
                    proxies=server.proxies,
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

        # server config goes in the upper level
        if self.server.config:
            result.update(self.server.config.as_dict)

        # output config goes in "output"
        # and decides where its sub-configs go through its as_dict property
        # (e.g. PDFConfigs are just appended at this "output" level)
        result["output"] = self.output_config.as_dict

        result["template"] = self.template.template_dict

        # TODO: support REST endpoint as template file source (see docs)
        # => Should be an extra Resource,
        #    but the problem is these Resource objects can represent both
        #    template files and prepend/append/subtemplate files.
        #    From the docs, it looks like it's only supported for templates.
        #    So it could be a Resource type that e.g. raises TypeError in its secondary_file_dict property getter,
        #    but there might be a cleaner way.

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
