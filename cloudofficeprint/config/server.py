import logging
import requests
from typing import Mapping, Dict
from urllib.parse import urljoin, urlparse
import json


class Printer:
    """This class defines an IP-enabled printer to use with the Cloud Office Print server."""

    def __init__(self,
                 location: str,
                 version: str,
                 requester: str = "Cloud Office Print",
                 job_name: str = "Cloud Office Print"):
        """
        Args:
            location (str): IP address of the printer.
            version (str): IPP version.
            requester (str, optional): The name of the requester. Defaults to "Cloud Office Print".
            job_name (str, optional): The name of the print job. Defaults to "Cloud Office Print".
        """
        self.location: str = location
        self.version: str = version
        self.requester: str = requester
        self.job_name: str = job_name

    @property
    def _dict(self) -> Dict[str, str]:
        """The dict representation of this Printer object.

        Returns:
            Dict[str, str]: dict representation of this Printer object
        """
        return {
            "location": self.location,
            "version": self.version,
            "requester": self.requester,
            "job_name": self.job_name
        }


class Command:
    """Command object with a single command for the Cloud Office Print server."""

    def __init__(self,
                 command: str,
                 parameters: Mapping[str, str] = None):
        """
        Args:
            command (str): The name of the command to execute. This command should be present in the aop_config.json file.
            parameters (Mapping[str, str], optional): The parameters for the command. Defaults to None.
        """
        self.command: str = command
        self.parameters: Dict[str, str] = dict(parameters)

    @property
    def _dict(self) -> Dict[str, str]:
        """The dict representation of this command.

        Returns:
            Dict[str, str]: dict representation of this command
        """
        result = {
            "command": self.command
        }

        if self.parameters:
            result["command_parameters"] = self.parameters

        return result

    @property
    def _dict_pre(self) -> Dict[str, str]:
        """The dict representation of this command, but 'pre' is prepended to the keys. This is used for pre-conversion commands.

        Returns:
            Dict[str, str]: dict representation of this command, with 'pre' prepended to the keys
        """
        return {"pre_" + k: v for k, v in self._dict.items()}

    @property
    def _dict_post(self) -> Dict[str, str]:
        """The dict representation of this command, but 'post' is prepended to the keys. This is used for post-process, post-conversion and post-merge commands.

        Returns:
            Dict[str, str]: dict representation of this command, with 'post' prepended to the keys
        """
        return {"post_" + k: v for k, v in self._dict.items()}


class Commands:
    """Command hook configuration class."""

    def __init__(self,
                 post_process: Command = None,
                 post_process_return: bool = None,
                 post_process_delete_delay: int = None,
                 pre_conversion: Command = None,
                 post_conversion: Command = None,
                 post_merge: Command = None):
        """
        Args:
            post_process (Command, optional): Command to run after the given request has been processed but before returning back the output file. Defaults to None.
            post_process_return (bool, optional): Whether to return the output or not. Note this output is Cloud Office Print's output and not the post process command output. Defaults to None.
            post_process_delete_delay (int, optional): Cloud Office Print deletes the file provided to the command directly after executing it. This can be delayed with this option. Integer in milliseconds. Defaults to None.
            pre_conversion (Command, optional): Command to run before conversion. Defaults to None.
            post_conversion (Command, optional): Command to run after conversion. Defaults to None.
            post_merge (Command, optional): Command to run after merging has happened. Defaults to None.
        """
        self.post_process: Command = post_process
        self.post_process_return: bool = post_process_return
        self.post_process_delete_delay: int = post_process_delete_delay
        self.pre_conversion: Command = pre_conversion
        self.post_conversion: Command = post_conversion
        self.post_merge: Command = post_merge

    @property
    def _dict(self) -> Dict:
        """The dict representation of this Commands object.

        Returns:
            Dict: dict representation of this Commands object
        """
        result = {}

        if self.post_process:
            to_add = self.post_process._dict
            if self.post_process_return is not None:
                to_add["return_output"] = self.post_process_return
            if self.post_process_delete_delay is not None:
                to_add["delete_delay"] = self.post_process_delete_delay
            result["post_process"] = to_add

        if self.pre_conversion or self.post_conversion:
            result["conversion"] = {}
            if self.pre_conversion:
                result["conversion"].update(self.pre_conversion._dict_pre)
            if self.post_conversion:
                result["conversion"].update(self.post_conversion._dict_post)

        if self.post_merge:
            result["merge"] = self.post_merge._dict_post

        return result


class ServerConfig:
    """Class for configuring the server options."""

    def __init__(self,
                 api_key: str = None,
                 logging: Mapping = None,
                 printer: Printer = None,
                 commands: Commands = None,
                 proxies: Dict[str, str] = None,
                 cop_remote_debug: bool = False):
        """
        Args:
            api_key (str, optional): API key to use for communicating with a Cloud Office Print server. Defaults to None.
            logging (Mapping, optional): Additional key/value pairs you would like to have logged into server_printjob.log on the server. (To be used with the --enable_printlog server flag). Defaults to None.
            printer (Printer, optional): IP printer to use with this server. See the Cloud Office Print docs for more info and supported printers. Defaults to None.
            commands (Commands, optional): Configuration for the various command hooks offered. Defaults to None.
            proxies (Dict[str, str], optional): Proxies for contacting the server URL, [as a dictionary](https://requests.readthedocs.io/en/master/user/advanced/#proxies). Defaults to None.
            cop_remote_debug (bool, optional): If True: The Cloud Office Print server will log the JSON into the database and this can bee seen when logged into cloudofficeprint.com. Defaults to False.
        """
        self.api_key: str = api_key
        self.logging: dict = dict(logging) if logging else None
        self.proxies: Dict[str, str] = proxies
        self.printer: Printer = printer
        self.commands: Commands = commands
        self.cop_remote_debug: bool = cop_remote_debug

    @property
    def as_dict(self) -> Dict:
        """The dict representation of these server configurations.

        Returns:
            Dict: the dict representation of these server configurations
        """
        result = {}

        if self.api_key is not None:
            result["api_key"] = self.api_key
        if self.logging is not None:
            result["logging"] = self.logging
        if self.printer is not None:
            result["ipp"] = self.printer._dict
        if self.cop_remote_debug:
            result['aop_remote_debug'] = 'Yes'

        if self.commands is not None:
            result.update(self.commands._dict)

        return result


class Server:
    """This config class is used to specify the Cloud Office Print server to interact with."""

    def __init__(self, url: str, config: ServerConfig = None):
        """
        Args:
            url (str): Server URL.
            config (ServerConfig): Server configuration.
        """
        self.url = url
        self.config: ServerConfig = config

    @property
    def url(self) -> str:
        """URL at which to contact the server.

        Returns:
            str: URL at which to contact the server
        """
        return self._url

    @url.setter
    def url(self, value: str):
        """Setter for the URL at which to contact the server.

        Args:
            value (str): URL at which to contact the server
        """
        if (urlparse(value).scheme == ''):
            self._url = "http://" + value
            logging.warning(
                f'No scheme found in "{value}", assuming "{self._url}".')
        else:
            self._url = value

    def is_reachable(self) -> bool:
        """Contact the server to see if it is reachable.

        Returns:
            bool: whether the server at `Server.url` is reachable
        """
        try:
            r = requests.get(urljoin(
                self.url, "marco"), proxies=self.config.proxies if self.config is not None else None)
            return r.text == "polo"
        except requests.exceptions.ConnectionError:
            return False

    def _raise_if_unreachable(self):
        """Raise a connection error if the server is unreachable.

        Raises:
            ConnectionError: raise error if server is unreachable
        """
        if not self.is_reachable():
            raise ConnectionError(
                f"Could not reach server at {self.url}")

    def get_version_soffice(self) -> str:
        """Sends a GET request to server-url/soffice.

        Returns:
            str: current version of Libreoffice installed on the server.
        """
        self._raise_if_unreachable()
        return requests.get(urljoin(self.url, 'soffice'), proxies=self.config.proxies if self.config is not None else None).text

    def get_version_officetopdf(self) -> str:
        """Sends a GET request to server-url/officetopdf.

        Returns:
            str: current version of OfficeToPdf installed on the server. (Only available if the server runs in Windows environment).
        """
        self._raise_if_unreachable()
        return requests.get(urljoin(self.url, 'officetopdf'), proxies=self.config.proxies if self.config is not None else None).text

    def get_supported_template_mimetypes(self) -> Dict:
        """Sends a GET request to server-url/supported_template_mimetypes.

        Returns:
            Dict: JSON of the mime types of templates that Cloud Office Print supports.
        """
        self._raise_if_unreachable()
        return json.loads(requests.get(urljoin(self.url, 'supported_template_mimetypes'), proxies=self.config.proxies if self.config is not None else None).text)

    def get_supported_output_mimetypes(self, input_type: str) -> Dict:
        """Sends a GET request to server-url/supported_output_mimetypes?template=input_type.
        Note: You will get empty JSON if the template extension isn't supported.

        Args:
            input_type (str): extension of file

        Returns:
            Dict: JSON of the supported output types for the given template extension.
        """
        self._raise_if_unreachable()
        return json.loads(requests.get(urljoin(self.url, 'supported_output_mimetypes' + f'?template={input_type}'), proxies=self.config.proxies if self.config is not None else None).text)

    def get_supported_prepend_mimetypes(self) -> Dict:
        """Sends a GET request to server-url/supported_prepend_mimetypes.

        Returns:
            Dict: JSON of the supported prepend file mime types.
        """
        self._raise_if_unreachable()
        return json.loads(requests.get(urljoin(self.url, 'supported_prepend_mimetypes'), proxies=self.config.proxies if self.config is not None else None).text)

    def get_supported_append_mimetypes(self) -> Dict:
        """Sends a GET request to server-url/supported_append_mimetypes.

        Returns:
            Dict: JSON of the supported append file mime types.
        """
        self._raise_if_unreachable()
        return json.loads(requests.get(urljoin(self.url, 'supported_append_mimetypes'), proxies=self.config.proxies if self.config is not None else None).text)

    def get_version_cop(self) -> str:
        """Sends a GET request to server-url/version.

        Returns:
            str: the version of Cloud Office Print that the server runs.
        """
        self._raise_if_unreachable()
        return requests.get(urljoin(self.url, 'version'), proxies=self.config.proxies if self.config is not None else None).text
