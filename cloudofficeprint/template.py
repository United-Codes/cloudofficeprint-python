import json
from typing import Dict

from . import Resource


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
        """Create a new Template

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
        self.template_hash = template_hash
        self.should_hash = False

    def reset_hash(self, should_hash: bool = True):
        self.template_hash = None
        self.should_hash = should_hash

    @property
    def mimetype(self) -> str:
        return self.resource.mimetype

    @property
    def template_json(self) -> str:
        return json.dumps(self.template_dict)

    @property
    def template_dict(self) -> Dict:
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
        return self.template_json

    @staticmethod
    def from_base64(
        base64string: str,
        filetype: str,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        return Template(
            Resource.from_base64(base64string, filetype),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )

    @staticmethod
    def from_raw(
        raw_data: bytes,
        filetype: str,
        start_delimiter: str = None,
        end_delimiter: str = None,
        should_hash: bool = None,
        template_hash: str = None,
    ) -> "Template":
        return Template(
            Resource.from_raw(raw_data, filetype),
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
        return Template(
            Resource.from_html(htmlstring, landscape),
            start_delimiter,
            end_delimiter,
            should_hash,
            template_hash,
        )
