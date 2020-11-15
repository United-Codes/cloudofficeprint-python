import logging
import requests
from typing import Mapping, Dict
from urllib.parse import urljoin, urlparse


class Printer:
    """This class defines an IP-enabled printer to use with the AOP server."""

    def __init__(self,
                 location: str,
                 version: str,
                 requester: str = "AOP",
                 job_name: str = "AOP"):
        self.location: str = location
        self.version: str = version
        self.requester: str = requester
        self.job_name: str = job_name

    @property
    def _dict(self) -> Dict[str, str]:
        return {
            "location": self.location,
            "version": self.version,
            "requester": self.requester,
            "job_name": self.job_name
        }


class Command:
    def __init__(self,
                 command: str,
                 args: Mapping[str, str] = None):
        self.command: str = command
        self.args: Dict[str, str] = dict(args)

    @property
    def _dict(self) -> Dict[str, str]:
        result = {
            "command": self.command
        }

        if self.args:
            result["args"] = self.args

        return result

    @property
    def _dict_pre(self) -> Dict[str, str]:
        return {"pre_" + k: v for k, v in self._dict.items()}

    @property
    def _dict_post(self) -> Dict[str, str]:
        return {"post_" + k: v for k, v in self._dict.items()}


class Commands:
    """Command hook configuration class. The command should be present in the aop_config.json file."""
    def __init__(self,
                 post_process: Command = None,
                 post_process_return: bool = None,
                 post_process_delete_delay: int = None,
                 pre_conversion: Command = None,
                 post_conversion: Command = None,
                 post_merge: Command = None):
        """
        Args:
            post_process (Command, optional): `Commands.post_process`. Defaults to None.
            post_process_return (bool, optional): `Commands.post_process_return`. Defaults to None.
            post_process_delete_delay (int, optional): `Commands.post_process_delete_delay`. Defaults to None.
            pre_conversion (Command, optional): `Commands.pre_conversion`. Defaults to None.
            post_conversion (Command, optional): `Commands.post_conversion`. Defaults to None.
            post_merge (Command, optional): `Commands.post_merge`. Defaults to None.
        """
        self.post_process: Command = post_process
        """Command to run after post processing."""
        self.post_process_return: bool = post_process_return
        """Whether to return the output or not. Note this output is AOP's output and not the post process command output."""
        self.post_process_delete_delay: int = post_process_delete_delay
        """AOP deletes the file provided to the command directly after executing it. This can be delayed with this option. Integer in milliseconds."""
        self.pre_conversion: Command = pre_conversion
        """Command to run before conversion."""
        self.post_conversion: Command = post_conversion
        """Command to run after conversion."""
        self.post_merge: Command = post_merge
        """Command to run after merging has happened"""

    @property
    def _dict(self):
        result = {}

        if self.post_process:
            to_add = self.post_process._dict
            if self.post_process_return:
                to_add["return_output"] = self.post_process_return
            if self.post_process_delete_delay:
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
    def __init__(self,
                 api_key: str = None,
                 logging: Mapping = None,
                 printer: Printer = None,
                 commands: Commands = None,
                 proxies: Dict[str, str] = None):
        self.api_key: str = api_key
        """API key to use for the application."""
        self.logging: dict = dict(logging) if logging else None
        """
        Additional key/value pairs you would like to have logged into server_printjob.log on the server.
        (To be used with the --enable_printlog server flag)
        """
        self.proxies = proxies
        """Proxies for contacting the server URL,
        [as a dictionary](https://requests.readthedocs.io/en/master/user/advanced/#proxies)"""
        self.printer: Printer = printer
        """IP printer to use with this server. See the AOP docs for more info and supported printers."""
        self.commands: Commands = commands
        """Configuration for the various command hooks offered."""

    @property
    def as_dict(self):
        result = {}

        if self.api_key:
            result["api_key"] = self.api_key
        if self.logging:
            result["logging"] = self.logging
        if self.printer:
            result["ipp"] = self.printer._dict

        if self.commands is not None:
            result.update(self.commands._dict)

        return result


class Server:
    """This config class is used to specify the AOP server to interact with."""

    # TODO: get_version(), ... (there are some server statuses on other paths than /marco)

    def __init__(self, url: str, config: ServerConfig = None):
        """
        Args:
            url (str): `Server.url`.
            proxies (Dict[str, str]): `Server.proxies`
            config (ServerConfig): `Server.config`
        """
        self.url = url
        """Server URL."""
        self.config: ServerConfig = config
        """Server configuration."""

    @property
    def url(self) -> str:
        """URL at which to contact the server."""
        return self._url

    @url.setter
    def url(self, value: str):
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
            r = requests.get(urljoin(self.url, "marco"), proxies=self.config.proxies)
            return r.text == "polo"
        except requests.exceptions.ConnectionError:
            return False

    def _raise_if_unreachable(self):
        if not self.is_reachable():
            raise ConnectionError(
                f"Could not reach server at {self.url}")
