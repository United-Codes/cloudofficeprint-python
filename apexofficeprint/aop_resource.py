import base64
import requests
import mimetypes
from os import path
from urllib.parse import urlparse

_supported_template_mimetypes = [
    "text/plain",
    "text/markdown",
    "text/html",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
]

class AOPResource:
    def __init__(self):
        self._data_type = None
        self._data = None
        self._filename = None
        self._mimetype = None

    @property
    def mimetype(self):
        return self._mimetype

    @property
    def filename(self):
        return self._filename

    @mimetype.setter
    def mimetype(self, value):
        if self.is_supported_mimetype(value):
            self._mimetype = value
        else:
            raise TypeError(f'Unsupported mime type: "{value}"')

    @property
    def data_type(self):
        return self._data_type

    @property
    def data(self):
        return self._data

    def to_base64(self):
        if (self.data_type is "base64"):
            return self.data
        elif (self.data_type is "raw"):
            return base64.b64encode(self.data).decode("ascii")
        else:
            # it should not be possible to load an unsupported data type in the first place
            raise NotImplementedError(f'Data type {self.data_type} has no base64 conversion implementation. This should not happen.')

    def load_base64(self, base64string):
        self._data_type = "base64"
        self._data = base64string

    def load_raw(self, binary_data):
        self._data_type = "raw"
        self._data = binary_data

    def load_local_file(self, local_file_path):
        try:
            f = open(local_file_path, "rb")
            self._data = f.read()
            self._data_type = "raw"
            self._mimetype = mimetypes.guess_type(local_file_path)[0]
            # strip the path leading up to the file and the extension, leaving only the file name
            self._filename = path.splitext(path.split(local_file_path)[1])[0]
        except IOError:
            pass
        finally:
            f.close()

    def load_url(self, url, proxies=None):
        """
        proxies is a dict containing the proxy type as key and the url as value.
        examples (from https://requests.readthedocs.io/en/master/user/advanced/#proxies):
            'http': 'http://10.10.1.10:3128',
            'https': 'http://10.10.1.10:1080',
            'http': 'http://user:pass@10.10.1.10:3128/',
            'http://10.20.1.128': 'http://10.10.1.10:5323' # set proxy for a specific host
            'https': 'socks5://user:pass@host:port'
        """
        r = requests.get(url, proxies=proxies, allow_redirects=True)
        self._data = r.content
        self._data_type = "raw"
        filename = path.basename(urlparse(url))
        self._mimetype = mimetypes.guess_type(filename)[0]
        self._filename = path.splitext(filename)[0] # strip extension

    @staticmethod
    def is_supported_mimetype(mimetype):
        return mimetype in _supported_template_mimetypes
