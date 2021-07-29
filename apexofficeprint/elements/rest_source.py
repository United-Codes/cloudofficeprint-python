from abc import ABC, abstractmethod
from typing import Dict, List, Union, FrozenSet, Iterable, Mapping

class RESTSource(ABC):
    """Abstract base class for REST datasources."""
    def __init__(self, datasource: str, endpoint: str, filename: str=None, headers: List[Mapping[str, str]]=None, auth: str=None):
        """
        Args:
            datasource (str): Type of request: graphql or rest.
            endpoint (str): URL of the data source from where the JSON needs to be read.
            filename (str, optional): Name of the output file. Defaults to None.
            headers (List[Mapping[str, str]], optional): HTTP headers, e.g. [{"Content-Type":"application/json"},{"Custom-Auth-Token":"xysazxklj4568asdf46a5sd4f"}]. Defaults to None.
            auth (str, optional): Basic authentication i.e. 'user:password' to compute an Authorization header. Defaults to None.
        """
        self.datasource: str = datasource
        self.endpoint: str = endpoint
        self.filename: str = filename
        self.headers: List[Mapping[str, str]] = headers
        self.auth: str = auth
        
    
    @property
    @abstractmethod
    def as_dict(self) -> Dict:
        """Dictionary representation of this RESTSource object.

        Returns:
            Dict: dictionary representation of this RESTSource object
        """
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
        """
        Args:
            endpoint (str): URL of the data source from where the JSON needs to be read.
            method (str, optional): HTTP method. Defaults to 'GET'.
            body (str, optional): Body of HTTP request (can be left empty for GET requests). Defaults to ''.
            filename (str, optional): Name of the output file. Defaults to None.
            headers (List[Mapping[str, str]], optional): HTTP headers, e.g. [{"Content-Type":"application/json"},{"Custom-Auth-Token":"xysazxklj4568asdf46a5sd4f"}]. Defaults to None.
            auth (str, optional): Basic authentication i.e. 'user:password' to compute an Authorization header. Defaults to None.
        """
        super().__init__(datasource='rest', endpoint=endpoint, filename=filename, headers=headers, auth=auth)
        self.method: str = method
        self.body: str = body
    
    @property
    def as_dict(self) -> Dict:
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
        """
        Args:
            endpoint (str): URL of the data source from where the JSON needs to be read.
            query (str): Graphql query.
            filename (str, optional): Name of the output file. Defaults to None.
            headers (List[Mapping[str, str]], optional): HTTP headers, e.g. [{"Content-Type":"application/json"},{"Custom-Auth-Token":"xysazxklj4568asdf46a5sd4f"}]. Defaults to None.
            auth (str, optional): Basic authentication i.e. 'user:password' to compute an Authorization header. Defaults to None.
        """
        super().__init__('graphql', endpoint, filename=filename, headers=headers, auth=auth)
        self.query: str = query
        

    @property
    def as_dict(self) -> Dict:
        result = super().as_dict

        result['query'] = self.query

        return result