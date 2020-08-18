"""
Module containing the Response class, which is also exposed at package level.
"""

import requests
from ._utils import type_utils
from os.path import splitext

class Response():
    """The Response class serves as a container for and interface with the AOP server's response to a printjob request.

    The AOP server can also throw an error, in which case you will be dealing with an apexofficeprint.exceptions.AOPError instead of this class.
    """

    def __init__(self, response: requests.Response):
        """You should never need to construct a Response manually.

        Args:
            response (requests.Response): Response object from the requests package
        """
        self._mimetype = response.headers["Content-Type"]
        self._bytes = response.content

    @property
    def mimetype(self) -> str:
        """Mime type of this response."""
        return self._mimetype

    @property
    def filetype(self) -> str:
        """File type (extension) of this response. E.g. "docx"."""
        return type_utils.mimetype_to_extension(self.mimetype)

    @property
    def binary(self) -> bytes:
        """Binary representation of the output file.

        Response.to_file can be used to output to a file,
        alternatively, use this property to do something else with the binary data.

        Returns:
            bytes: response file as binary
        """
        return self._bytes

    def to_file(self, path: str):
        """Write the response to a file at the given path without extension.

        If the given file path does not contain an extension,
        the correct path is automatically added from the response data.
        That is how this method is intended to be used.
        You should only specify the extension in the path if you have some reason to specify the extension manually.

        Args:
            path (str): path without extension
        """

        if not splitext(path)[1]:
            path += "." + self.filetype

        # open the file in binary ("b") and write ("w") mode
        outfile = open(path, "wb")
        outfile.write(self.binary)
        outfile.close()
