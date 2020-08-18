import base64
import requests
from typing import BinaryIO


def raw_to_base64(raw_data) -> str:
    """Convert raw data to a base64 string.

    Args:
        raw_data: a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object)

    Returns:
        str: base64 string
    """
    return base64.b64encode(raw_data).decode("ascii")


def read_file_as_base64(path: str) -> str:
    """Read a local file as base64 string.

    Args:
        path (str): local path

    Returns:
        str: base64 string
    """
    f = open(path, "rb")
    file_content = f.read()
    f.close()
    return raw_to_base64(file_content)


def url_as_base64(url: str) -> str:
    """Fetch content at url as base64.

    Args:
        url (str): URL

    Returns:
        str: base64 string
    """
    return raw_to_base64(requests.get(url, stream=True).raw)
