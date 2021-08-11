import apexofficeprint as aop
from test import server


def test_rest_source_rest():
    data = aop.elements.RESTSourceREST(
        endpoint='endpoint_url',
        method='GET',
        body='',
        filename='output_file',
        headers=[{"Content-Type":"application/json"}],
        auth='username:password'
    )
    data_expected = {
        'filename': 'output_file',
        'datasource': 'rest',
        'method': 'GET',
        'body': '',
        'endpoint': 'endpoint_url',
        'headers': [{"Content-Type":"application/json"}],
        'auth': 'username:password'
    }
    assert data.as_dict == data_expected


def test_rest_source_graphql():
    data = aop.elements.RESTSourceGraphQL(
        endpoint='endpoint_url',
        query='test_query',
        filename='output_file',
        headers=[{"Content-Type":"application/json"}],
        auth='username:password'
    )
    data_expected = {
        'filename': 'output_file',
        'datasource': 'graphql',
        'query': 'test_query',
        'endpoint': 'endpoint_url',
        'headers': [{"Content-Type":"application/json"}],
        'auth': 'username:password'
    }
    assert data.as_dict == data_expected


def test_rest_source_printjob():
    data = aop.elements.RESTSourceREST(
        endpoint='endpoint_url',
        method='GET',
        body='',
        filename='output_file',
        headers=[{"Content-Type":"application/json"}],
        auth='username:password'
    )
    pj = aop.PrintJob(
        data=data,
        server=server,
        template=aop.Resource.from_base64('test_base64', 'docx'),
    )
    pj_expected = {
        'tool': 'python',
        'python_sdk_version': aop.printjob.STATIC_OPTS['python_sdk_version'],
        'api_key': server.config.api_key,
        'output': {
            'output_converter': 'libreoffice',
            'output_encoding': 'raw',
            'output_type': 'docx'
        },
        'template': {
            'template_type': 'docx',
            'file': 'test_base64'
        },
        'files': [
            {
                'filename': 'output_file',
                'datasource': 'rest',
                'method': 'GET',
                'body': '',
                'endpoint': 'endpoint_url',
                'headers': [{"Content-Type":"application/json"}],
                'auth': 'username:password'
            }
        ]
    }
    assert pj.as_dict == pj_expected

def run():
    test_rest_source_rest()
    test_rest_source_graphql()
    test_rest_source_printjob()

if __name__ == '__main__':
    run()
