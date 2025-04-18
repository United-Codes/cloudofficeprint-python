# import cloudofficeprint as cop

import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop



def compare_dicts(dict1, dict2, path=""):
    """
    Recursively compare two dictionaries and log differences.
    """
    for key in dict1.keys():
        if key not in dict2:
            print(f"Key '{path + key}' found in dict1 but not in dict2.")
        else:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                # Recursively compare nested dictionaries
                compare_dicts(dict1[key], dict2[key], path + key + ".")
            elif dict1[key] != dict2[key]:
                print(f"Difference at '{path + key}':")




def test_printjob():
    """Test all options for printjob"""

    SERVER_URL = "https://api.cloudofficeprint.com/"
    API_KEY = "YOUR_API_KEY"

    server = cop.config.Server(SERVER_URL, cop.config.ServerConfig(api_key=API_KEY))

    resource = cop.Resource.from_local_file("./tests/data/template.docx")
    template = cop.Template.from_local_file(
        "./tests/data/template_prepend_append_subtemplate.docx"
    )

    resource_base64 = resource.data
    template_base64 = template.resource.data

    data = cop.elements.ElementCollection("data")
    data.add(cop.elements.Property("textTag1", "test_text_tag1"))

    output_conf = cop.config.OutputConfig(filetype="pdf")

    printjob = cop.PrintJob(
        data=data,
        server=server,
        template=template,
        output_config=output_conf,
        compare_files=[resource, template.resource]
    )

    printjob_expected = {
        "tool": "python",
        "python_sdk_version": cop.printjob.STATIC_OPTS["python_sdk_version"],
        "api_key": server.config.api_key,
        "output": {
            "output_converter": "libreoffice",
            "output_encoding": "raw",
            "output_type": "pdf",
        },
        "compare_files": [
            {
                "file_content": resource_base64,
                "file_source": "base64",
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            },
            {
                "file_content": template_base64,
                "file_source": "base64",
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            },
        ],
        "files": [{"data": {"textTag1": "test_text_tag1"}}],
        "template": {"file": template_base64, "template_type": "docx"}
    }


    assert printjob.as_dict == printjob_expected
    # printjob.execute().to_file("tests/data/prepend_append_subtemplate_test") # Works as expected

def test_pdf_attachment():
    """
    """
    SERVER_URL = "https://api.cloudofficeprint.com/"
    API_KEY = "YOUR_API_KEY"

    server = cop.config.Server(SERVER_URL, cop.config.ServerConfig(api_key=API_KEY))

    resource = cop.Resource.from_local_file("./tests/data/template.docx")
    template = cop.Template.from_local_file(
        "./tests/data/template_prepend_append_subtemplate.docx"
    )

    resource_base64 = resource.data
    template_base64 = template.resource.data

    data = cop.elements.ElementCollection("data")
    data.add(cop.elements.Property("textTag1", "test_text_tag1"))

    output_conf = cop.config.OutputConfig(filetype="pdf")

    printjob = cop.PrintJob(
        data=data,
        server=server,
        template=template,
        output_config=output_conf,
        attachments=[resource],
    )
    
    printjob_expected = {
        "api_key": server.config.api_key,
        "attachments": [
            {
                "file_content": resource_base64,
                "file_source": "base64",
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            }
        ],
        "files": [{"data": {"textTag1": "test_text_tag1"}}],
        "output": {
            "output_converter": "libreoffice",
            "output_encoding": "raw",
            "output_type": "pdf",
        },
        "template": {"file": template_base64, "template_type": "docx"},
        "tool": "python",
        "python_sdk_version": cop.printjob.STATIC_OPTS["python_sdk_version"],
    }
    
def test_template_hashing_printjob():
    """Test all options for printjob"""

    SERVER_URL = "https://api.cloudofficeprint.com/"
    API_KEY = "YOUR_API_KEY"

    server = cop.config.Server(SERVER_URL, cop.config.ServerConfig(api_key=API_KEY))

    template = cop.Template.from_local_file(
        "./tests/data/template_prepend_append_subtemplate.docx", None, None, True
    )

    template_base64 = template.resource.data

    data = cop.elements.ElementCollection("data")
    data.add(cop.elements.Property("textTag1", "test_text_tag1"))

    printjob = cop.PrintJob(data, server, template)

    printjob_expected = {
        "api_key": server.config.api_key,
        "files": [{"data": {"textTag1": "test_text_tag1"}}],
        "output": {
            "output_converter": "libreoffice",
            "output_encoding": "raw",
            "output_type": "docx",
        },
        "template": {
            "file": template_base64,
            "template_type": "docx",
            "should_hash": True,
        },
        "tool": "python",
        "python_sdk_version": cop.printjob.STATIC_OPTS["python_sdk_version"],
    }

    assert printjob.as_dict == printjob_expected

    template.update_hash("test_hash")

    printjob_expected_2 = {
        "api_key": server.config.api_key,
        "files": [{"data": {"textTag1": "test_text_tag1"}}],
        "output": {
            "output_converter": "libreoffice",
            "output_encoding": "raw",
            "output_type": "docx",
        },
        "template": {
            "template_type": "docx",
            "template_hash": "test_hash",
        },
        "tool": "python",
        "python_sdk_version": cop.printjob.STATIC_OPTS["python_sdk_version"],
    }

    assert printjob.as_dict == printjob_expected_2


def run():
    test_printjob()
    test_pdf_attachment()


if __name__ == "__main__":
    run()
