"""
Module containing the PrintJob class, which is also exposed at package level.
"""

import requests
import asyncio
import json

from typing import Union, List, Dict, Mapping
from functools import partial
from pprint import pprint

from .config import OutputConfig, Server
from .elements import Element, RESTSource
from .exceptions import COPError
from .resource import Resource
from .template import Template
from .response import Response

STATIC_OPTS = {
    "tool": "python",
    # "version": "18.2", # optional: version of Cloud Office Print JSON format
    "python_sdk_version": "21.2.0",
}


class PrintJob:
    """A print job for a Cloud Office Print server.

    This class contains all configuration options, resources, render elements ...
    and the `PrintJob.execute` method to combine all these and send a request to the Cloud Office Print server.
    """

    def __init__(
        self,
        data: Union[Element, Mapping[str, Element], RESTSource],
        server: Server,
        template: Union[Template, Resource] = None,
        output_config: OutputConfig = OutputConfig(),
        subtemplates: Dict[str, Resource] = {},
        prepend_files: List[Resource] = [],
        append_files: List[Resource] = [],
        attachments : List[Resource] = [],
        cop_verbose: bool = False,
    ):
        """
        Args:
            data (Union[Element, Mapping[str, Element], RESTSource]): This is either: An `Element` (e.g. an `ElementCollection`); A mapping, containing file names as keys and an `Element` as data. Multiple files will be produced from the different datas, the result is a zip file containing them. In the first case, no output file name is specified and the server will name it "file0".
            server (Server): Server to be used for this print job.
            template (Union[Template, Resource]): Template to use for this print job.
            output_config (OutputConfig, optional): Output configuration to be used for this print job. Defaults to `OutputConfig`().
            subtemplates (Dict[str, Resource], optional): Subtemplates for this print job, accessible (in docx) through `{?include subtemplate_dict_key}`. Defaults to {}.
            prepend_files (List[Resource], optional): Files to prepend to the output file. Defaults to [].
            append_files (List[Resource], optional): Files to append to the output file. Defaults to [].
            attachments (List[Resource], optional): Files to attach to the pdf file. Defaults to []. The file must be PDF.
            cop_verbose (bool, optional): Whether or not verbose mode should be activated. Defaults to False.
        """
        self.data: Union[Element, Mapping[str, Element], RESTSource] = data
        self.server: Server = server
        self.output_config: OutputConfig = output_config
        self.template: Union[Template, Resource] = template
        self.subtemplates: Dict[str, Resource] = subtemplates
        self.prepend_files: List[Resource] = prepend_files
        self.append_files: List[Resource] = append_files
        self.attachments: List[Resource] = attachments
        self.cop_verbose: bool = cop_verbose

    def execute(self) -> Response:
        """Execute this print job.

        Returns:
            Response: `Response`-object
        """
        self.server._raise_if_unreachable()
        proxy = self.server.config.proxies if self.server.config else None
        response = requests.post(
            self.server.url,
            json=self.as_dict,
            proxies=proxy,
            headers={"Content-type": "application/json"},
        )
        if type(self.template) is Template and self.template.should_hash:
            template_hash = response.headers["Template-Hash"]
            if template_hash:
                self.template.update_hash(template_hash)
        return self._handle_response(response)

    async def execute_async(self) -> Response:
        """Async version of `PrintJob.execute`

        Returns:
            Response: `Response`-object
        """
        self.server._raise_if_unreachable()
        proxy = self.server.config.proxies if self.server.config else None
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            partial(
                requests.post,
                self.server.url,
                json=self.as_dict,
                proxies=proxy,
                headers={"Content-type": "application/json"},
            ),
        )
        if type(self.template) is Template and self.template.should_hash:
            template_hash = response.headers["Template-Hash"]
            if template_hash:
                self.template.update_hash(template_hash)
        return PrintJob._handle_response(response)

    @staticmethod
    def execute_full_json(json_data: str, server: Server) -> Response:
        """If you already have the JSON to be sent to the server (not just the data, but the entire JSON body including your API key and template), this package will wrap the request to the server.

        Args:
            json_data (str): full JSON data that needs to be sent to a Cloud Office Print server
            server (Server): `Server`-object

        Returns:
            Response: `Response`-object
        """
        server._raise_if_unreachable()
        proxy = server.config.proxies if server.config else None
        response = requests.post(
            server.url,
            data=json_data,
            proxies=proxy,
            headers={"Content-type": "application/json"},
        )
        return PrintJob._handle_response(response)

    @staticmethod
    async def execute_full_json_async(json_data: str, server: Server) -> Response:
        """Async version of `Printjob.execute_full_json`

        Args:
            json_data (str): full JSON data that needs to be sent to a Cloud Office Print server
            server (Server): `Server`-object

        Returns:
            Response: `Response`-object
        """
        server._raise_if_unreachable()
        proxy = server.config.proxies if server.config else None
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            partial(
                requests.post,
                server.url,
                data=json_data,
                proxies=proxy,
                headers={"Content-type": "application/json"},
            ),
        )
        return PrintJob._handle_response(response)

    @staticmethod
    def _handle_response(res: requests.Response) -> Response:
        """Converts the HTML response to a `Response`-object

        Args:
            res (requests.Response): HTML response from the Cloud Office Print server

        Raises:
            COPError: Error when the HTML status code is not 200

        Returns:
            Response: `Response`-object of HTML response
        """
        if res.status_code != 200:
            raise COPError(res.text)
        else:
            return Response(res)

    @property
    def json(self) -> str:
        """JSON equivalent of the dict representation of this print job.
        This representation is isomorphic to the dict representation `Printjob.as_dict`.

        Returns:
            str: JSON equivalent of the dict representation of this print job
        """
        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> Dict:
        """Return the dict representation of this print job.

        Returns:
            Dict: dict representation of this print job
        """
        # Copy of STATIC_OPTS! Otherwise everything we add to 'result' will also be added to 'STATIC_OPTS'
        result = dict(STATIC_OPTS)
        # server config goes in the upper level
        if self.server.config:
            result.update(self.server.config.as_dict)

        # output config goes in "output"
        # and decides where its sub-configs go through its as_dict property
        # (e.g. PDFConfigs are just appended at this "output" level)
        result["output"] = self.output_config.as_dict

        if self.template:
            result["template"] = self.template.template_dict

        # If output_type is not specified, set this to the template filetype
        # If no template found: default docx
        if "output_type" not in self.output_config.as_dict.keys():
            if self.template:
                result["output"]["output_type"] = result["template"]["template_type"]
            else:
                result["output"]["output_type"] = "docx"

        if isinstance(self.data, Mapping):
            result["files"] = [
                {"filename": name, "data": data.as_dict}
                for name, data in self.data.items()
            ]
        elif isinstance(self.data, RESTSource):
            result["files"] = [self.data.as_dict]
        else:
            result["files"] = [{"data": self.data.as_dict}]

        if len(self.prepend_files) > 0:
            result["prepend_files"] = [
                file.secondary_file_dict for file in self.prepend_files
            ]

        if len(self.append_files) > 0:
            result["append_files"] = [
                file.secondary_file_dict for file in self.append_files
            ]
        if len(self.attachments) > 0:
            result["attachments"] = [
                file.secondary_file_dict for file in self.attachments
            ]

        if len(self.subtemplates) > 0:
            result["templates"] = [
                {**file.secondary_file_dict, "name": name}
                for name, file in self.subtemplates.items()
            ]

        # If verbose mode is activated, print the result to the terminal
        if self.cop_verbose:
            print("The JSON data that is sent to the Cloud Office Print server:\n")
            pprint(result)

        return result
