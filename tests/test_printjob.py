import cloudofficeprint as cop
from test import server


def test_printjob():
    """Test all options for printjob"""
    prepend_file = cop.Resource.from_local_file('./tests/data/template.docx')

    template = cop.Resource.from_local_file('./tests/data/template.docx')
    template_main = cop.Resource.from_local_file(
        './tests/data/template_prepend_append_subtemplate.docx')
    template_base64 = template.data
    template_main_base64 = template_main.data

    data = cop.elements.ElementCollection('data')
    text_tag = cop.elements.Property('textTag1', 'test_text_tag1')
    data.add(text_tag)

    append_file = cop.Resource.from_local_file('./tests/data/template.docx')

    subtemplates = {
        'sub1': template,
        'sub2': template
    }

    output_conf = cop.config.OutputConfig(filetype='pdf')

    printjob = cop.PrintJob(
        data=data,
        server=server,
        template=template_main,
        output_config=output_conf,
        subtemplates=subtemplates,
        prepend_files=[prepend_file],
        append_files=[append_file])
    printjob_expected = {
        'api_key': server.config.api_key,
        'append_files': [
            {
                'file_content': template_base64,
                'file_source': 'base64',
                'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
        ],
        'files': [
            {
                'data': {
                    'textTag1': 'test_text_tag1'
                }
            }
        ],
        'output': {
            'output_converter': 'libreoffice',
            'output_encoding': 'raw',
            'output_type': 'pdf'
        },
        'prepend_files': [
            {
                'file_content': template_base64,
                'file_source': 'base64',
                'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
        ],
        'template': {
            'file': template_main_base64,
            'template_type': 'docx'
        },
        'tool': 'python',
        'templates': [
            {
                'file_content': template_base64,
                'file_source': 'base64',
                'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'name': 'sub1'
            },
            {
                'file_content': template_base64,
                'file_source': 'base64',
                'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'name': 'sub2'
            }
        ],
        'python_sdk_version': cop.printjob.STATIC_OPTS['python_sdk_version']
    }
    assert printjob.as_dict == printjob_expected
    # printjob.execute().to_file("tests/data/prepend_append_subtemplate_test") # Works as expected


def run():
    test_printjob()


if __name__ == '__main__':
    run()
