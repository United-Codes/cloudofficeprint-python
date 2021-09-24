import json
from typing import Dict

from .resource import Resource


class Template:
    """The Template class"""

    def __init__(
        self,
        resource: Resource,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ):
        """Create a new Template.

        Args:
            resource (Resource): the resource of this template.
            start_delimiter (str, optional): the starting delimiter used in the template.
            end_delimiter (str, optional): the starting delimiter used in the template.
            should_hash (bool, optional): whether the template should be hashed on the server.
            template_hash (str, optional): the hash of the template.
        """
        self.resource = resource
        self.start_delimiter = start_delimiter
        self.end_delimiter = end_delimiter
        self.should_hash = should_hash
        self.template_hash = template_hash

    def update_hash(self, template_hash: str):
        """Update the Template to store a hash.
        On the next request to the server, the file data will not be sent, only the hash of the template.

        Args:
            template_hash (str): the hash of the template.
        """
        self.template_hash = template_hash
        self.should_hash = False

    def reset_hash(self, should_hash: bool = True):
        """Reset the stored hash of the template.

        Args:
            should_hash (bool, optional): whether the template should be hashed on the server. Defaults to True.
        """
        self.template_hash = None
        self.should_hash = should_hash

    @property
    def mimetype(self) -> str:
        """
        Returns:
            str: the mime type of the Resource
        """
        return self.resource.mimetype

    @property
    def template_json(self) -> str:
        """
        Returns:
            str: the JSON representation of this Resource.
        """
        return json.dumps(self.template_dict)

    @property
    def template_dict(self) -> Dict:
        """
        Returns:
            Dict: the dictionary representation of this Resource.
        """
        if self.template_hash and not self.should_hash:
            return {
                "template_type": self.resource.filetype,
                "template_hash": self.template_hash,
                "start_delimiter": self.start_delimiter,
                "end_delimiter": self.end_delimiter,
            }
        return {
            **self.resource.template_dict,
            "start_delimiter": self.start_delimiter,
            "end_delimiter": self.end_delimiter,
            "should_hash": self.should_hash,
            "template_hash": self.template_hash,
        }

    def __str__(self) -> str:
        """Override the string representation of this class to return the template-style json.

        Returns:
            str: the JSON representation of this resource as a template.
        """
        return self.template_json

    @staticmethod
    def from_raw(
        raw_data: bytes,
        filetype: str,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        """Create a Template with a RawResource from raw file data.

        Args:
            raw_data (bytes): the raw data as a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object).
            filetype (str): the file type (extension).
            start_delimiter (str, optional): the starting delimiter used in the template.
            end_delimiter (str, optional): the starting delimiter used in the template.
            should_hash (bool, optional): whether the template should be hashed on the server.
            template_hash (str, optional): the hash of the template.

        Returns:
            Template: the created Template.
        """
        return Template(
            Resource.from_raw(raw_data, filetype),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )

    @staticmethod
    def from_base64(
        base64string: str,
        filetype: str,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        """Create a Template with a Base64Resource from a base64 string.

        Args:
            base64string (str): the base64 encoded representation of a file.
            filetype (str): the file type (extension).
            start_delimiter (str, optional): the starting delimiter used in the template.
            end_delimiter (str, optional): the starting delimiter used in the template.
            should_hash (bool, optional): whether the template should be hashed on the server.
            template_hash (str, optional): the hash of the template.

        Returns:
            Template: the created Template.
        """
        return Template(
            Resource.from_base64(base64string, filetype),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )

    @staticmethod
    def from_local_file(
        local_path: str,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        """Create a Template with a Base64Resource with the contents of a local file.
        The filetype is determined by the extension of the file.

        Throws IOError if it can't read the file.

        Args:
            local_path (str): the path to local file.
            start_delimiter (str, optional): the starting delimiter used in the template.
            end_delimiter (str, optional): the starting delimiter used in the template.
            should_hash (bool, optional): whether the template should be hashed on the server.
            template_hash (str, optional): the hash of the template.

        Returns:
            Template: the created Template.
        """
        return Template(
            Resource.from_local_file(local_path),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )

    @staticmethod
    def from_server_path(
        path: str,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        """Create a Template with a ServerPathResource targeting a file on the server.
        The filetype is determined by the extension of the file.

        Args:
            path (str): the location of target file on the server.
            start_delimiter (str, optional): the starting delimiter used in the template.
            end_delimiter (str, optional): the starting delimiter used in the template.
            should_hash (bool, optional): whether the template should be hashed on the server.
            template_hash (str, optional): the hash of the template.

        Returns:
            Template: the created Template.
        """
        return Template(
            Resource.from_server_path(path),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )

    @staticmethod
    def from_url(
        url: str,
        filetype: str,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        """Create a Template with a URLResource targeting the file at a given url.

        Args:
            url (str): the file URL.
            filetype (str): the file type (extension).
            start_delimiter (str, optional): the starting delimiter used in the template.
            end_delimiter (str, optional): the starting delimiter used in the template.
            should_hash (bool, optional): whether the template should be hashed on the server.
            template_hash (str, optional): the hash of the template.

        Returns:
            Template: the created Template.
        """
        return Template(
            Resource.from_url(url, filetype),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )

    @staticmethod
    def from_html(
        htmlstring: str,
        landscape: bool = False,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        """Create a Template with a HTMLResource with html data in plain text.

        Args:
            htmlstring (str): the html content.
            landscape (bool, optional): whether or not to use the landscape option. Defaults to False.
            start_delimiter (str, optional): the starting delimiter used in the template.
            end_delimiter (str, optional): the starting delimiter used in the template.
            should_hash (bool, optional): whether the template should be hashed on the server.
            template_hash (str, optional): the hash of the template.

        Returns:
            Template: the created Template.
        """
        return Template(
            Resource.from_html(htmlstring, landscape),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )
