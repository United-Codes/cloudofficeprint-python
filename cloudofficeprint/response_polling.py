"""
Module containing the ResponsePolling class, which is also exposed at package level.
"""

import re
import json

from .config import Server
from .response import IResponse, Response


class ResponsePolling(IResponse):
    """The Response class serves as a container for and interface with the Cloud Office Print server's response to a polled print job request.

    The Cloud Office Print server can also throw an error, in which case you will be dealing with a cloudofficeprint.exceptions.COPError instead of this class.
    This class will throw an error when calling the property 'response' when the polled print job has not been processed.
    """

    def __init__(self,
                 server: Server,
                 uid: str,
                 secret_key: str = None,
                 ):
        """
        Args:
            server (Server): The Cloud Office Print server that has the response of the polled print job.
            uid (str): The unique identifier of the polled print job.
            secret_key (str): The secret key used to encrypt the polled print job. Optional
        """
        self.server: Server = server
        self.uid: str = uid
        self.secret_key: str = secret_key
        self._response = None

    @property
    def response(self) -> Response:
        """The response of the polled print job on the Cloud Office Print server.

        Returns:
            Response: response of the polled print job on the Cloud Office Print server.

        Raises:
            Exception: If the polled print job has not been processed.
        """
        if self._response is None:
            self._response = self.server.download(self.uid, self.secret_key)
        return self._response

    def delete(self):
        """Deletes the response of the polled print job on the Cloud Office Print server.

        """
        self.server.download(self.uid, self.secret_key, True)

    @property
    def mimetype(self) -> str:
        """Mime type of this response.

        Returns:
            str: mime type of this response
        """
        return self.response.mimetype

    @property
    def filetype(self) -> str:
        """File type (extension) of this response. E.g. "docx".

        Returns:
            str: file type of this response
        """
        return self.response.filetype

    @property
    def binary(self) -> bytes:
        """Binary representation of the output file.

        Response.to_file can be used to output to a file,
        alternatively, use this property to do something else with the binary data.

        Returns:
            bytes: response file as binary
        """
        return self.response.binary

    def to_string(self) -> str:
        """Return the string representation of this buffer.
        Useful if the server returns a JSON (e.g. for output_type 'count_tags').

        Raises:
            err: raise error is bytes cannot be decoded in utf-8

        Returns:
            str: string representation of this buffer
        """
        return self.response.to_string()

    def to_file(self, path: str):
        """Write the response to a file at the given path without extension.

        If the given file path does not contain an extension,
        the correct path is automatically added from the response data.
        That is how this method is intended to be used.
        You should only specify the extension in the path if you have some reason to specify the extension manually.

        Args:
            path (str): path without extension
        """
        return self.response.to_file(path)
