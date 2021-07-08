from abc import ABC, abstractmethod
from typing import List, Union, FrozenSet, Iterable, Mapping

class RESTSource(ABC):
    """Abstract base class for REST datasources."""
    def __init__(self, datasource: str, endpoint: str, filename: str=None, headers: List[Mapping[str, str]]=None, auth: str=None):
        self.datasource: str = datasource
        """Type of request: graphql or rest"""
        self.endpoint: str = endpoint
        """URL of the data source from where the JSON needs to be read"""
        self.filename: str = filename
        """Name of the output file"""
        self.headers: str = headers
        """HTTP headers, e.g. [{"Content-Type":"application/json"},{"Custom-Auth-Token":"xysazxklj4568asdf46a5sd4f"}]"""
        self.auth: str = auth
        """Basic authentication i.e. 'user:password' to compute an Authorization header."""
    
    @property
    @abstractmethod
    def as_dict(self) -> dict:
        result = {
            'datasource': self.datasource,
            'endpoint': self.endpoint
        }

        if self.filename is not None:
            result['filename'] = self.filename
        if self.headers is not None:
            result['headers'] = self.headers
        if self.auth is not None:
            result['auth'] = self.auth
        
        return result

class RESTSourceREST(RESTSource):
    """Class for working with a REST endpoint using a REST request"""
    def __init__(
        self,
        endpoint: str,
        method: str='GET',
        body: str='',
        filename: str=None,
        headers: List[Mapping[str, str]]=None,
        auth: str=None):
        super().__init__(datasource='rest', endpoint=endpoint, filename=filename, headers=headers, auth=auth)
        self.method: str = method
        """HTTP method"""
        self.body: str = body
        """Body of HTTP request (can be left empty for GET requests)"""
    
    @property
    def as_dict(self) -> dict:
        result = super().as_dict

        result['method'] = self.method
        result['body'] = self.body

        return result

class RESTSourceGraphQL(RESTSource):
    """Class for working with a REST endpoint using a GraphQL request"""
    def __init__(
        self,
        endpoint: str,
        query: str,
        filename: str=None,
        headers: List[Mapping[str, str]]=None,
        auth: str=None):
        super().__init__('graphql', endpoint, filename=filename, headers=headers, auth=auth)
        self.query: str = query
        """Graphql query"""

    @property
    def as_dict(self) -> dict:
        result = super().as_dict

        result['query'] = self.query

        return result