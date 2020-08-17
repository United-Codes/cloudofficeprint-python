import json
import requests
from typing import Union
from .config import ServerConfig, OutputConfig
from .exceptions import AOPError
from .resource import Resource
from .response import Response

STATIC_OPTS = {
    "tool": "python"
    # "version": "18.2" # optional
}

# TODO: somewhere, this class should check whether its templates are compatible and whether they are in turn compatible with the output file type


class PrintJob:
    """# TODO: document
    """
    def __init__(self,
                 template: Resource,
                 server_config: ServerConfig,
                 output_config: OutputConfig = None):
        self._server_config = server_config
        self._output_config = output_config if output_config else OutputConfig()
        self._template = template

    def execute(self) -> Union[Response, AOPError]:
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
        to send to the server.

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
            json.loads('{"data":{"chartData":{"title":"aop chart title","xAxis":{"title":"aop x ax title","data":["string",2,3,4,5]},"yAxis":{"title":"aop y ax title","series":[{"name":"yseries1","data":[5,4,7,8,6]},{"name":"yseries2","data":[4,8,7,6,3]},{"name":"yseries3","data":[2,4,4,1,6]}]}},"secondAxesData":{"title":"aop chart title","xAxis":{"title":"aop x ax title","data":["string",2,3,4,5]},"x2Axis":{"title":"aop x2 ax title"},"yAxis":{"title":"aop y ax title","series":[{"name":"yseries1","data":[5,4,7,8,6]},{"name":"yseries2","data":[4,8,7,6,3]},{"name":"y2series","data":[2,4,4,1,6]}]},"y2Axis":{"title":"aop y2 ax title"}},"stockChartData":{"title":"aop stock chart title","xAxis":{"title":"aop x ax title","date":{"format":"d/m/yyyy","unit":"days","step":"1"},"data":["1999-05-16","1999-05-17","1999-05-18","1999-05-19","1999-05-20"]},"yAxis":{"title":"aop y ax title","series":[{"name":"volume","data":[148,135,150,120,70]},{"name":"open","data":[34,50,38,25,44]},{"name":"high","data":[58,58,57,57,55]},{"name":"low","data":[25,11,13,12,11]},{"name":"close","data":[43,35,50,38,25]}]}}}}')
        ]
        return result

    @property
    def server_config(self) -> ServerConfig:
        """Server configuration to be used for this print job.

        Should be an instance of apexofficeprint.config.ServerConfig

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

        Should be an instance of apexofficeprint.Resource

        Returns:
            Resource: resource to use as template
        """
        return self._template

    @template.setter
    def template(self, resource: Resource):
        self._template = resource
