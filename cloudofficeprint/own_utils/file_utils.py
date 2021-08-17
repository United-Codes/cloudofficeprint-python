import base64
import requests


def raw_to_base64(raw_data: bytes) -> str:
    """Convert raw data to a base64 string.

    Args:
        raw_data (bytes): a [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object) containing the raw data

    Returns:
        str: base64 string of the raw data
    """
    return base64.b64encode(raw_data).decode("ascii")


def read_file_as_base64(path: str) -> str:
    """Read a local file as base64 string.

    Args:
        path (str): path of the local file

    Returns:
        str: base64 representation of the file
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
        str: base64 representation of the content at the URL
    """
    return raw_to_base64(requests.get(url, stream=True).raw)
