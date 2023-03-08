import pathlib

import cloudofficeprint as cop


def test_resource_raw():
    local_path = str(pathlib.Path().resolve()) + "/tests/data/template.docx"
    with open(local_path, "rb") as f:
        content = f.read()
    resource = cop.Resource.from_raw(content, "docx")
    resource_expected = {
        "file": cop.own_utils.raw_to_base64(content),
        "template_type": "docx",
    }
    assert resource.template_dict == resource_expected


def test_resource_base64():
    resource = cop.Resource.from_base64("dummy", "docx")
    resource_expected = {"file": "dummy", "template_type": "docx"}
    assert resource.template_dict == resource_expected


def test_resource_local_file():
    local_path = str(pathlib.Path().resolve()) + "/tests/data/template.docx"
    resource = cop.Resource.from_local_file(local_path)
    with open(local_path, "rb") as f:
        content = f.read()
    resource_expected = {
        "file": cop.own_utils.raw_to_base64(content),
        "template_type": "docx",
    }
    assert resource.template_dict == resource_expected


def test_resource_server_path():
    resource = cop.Resource.from_server_path("dummy/path.docx")
    resource_expected = {"filename": "dummy/path.docx", "template_type": "docx"}
    assert resource.template_dict == resource_expected


def test_resource_url():
    resource = cop.Resource.from_url("dummy_url", "docx")
    resource_expected = {"template_type": "docx", "url": "dummy_url"}
    assert resource.template_dict == resource_expected


def test_resource_html():
    html_string = """
     <!DOCTYPE html>
    <html>
    <body>

    <h1>My First Heading</h1>
    <p>My first paragraph.</p>

    </body>
    </html> 
    """
    resource = cop.Resource.from_html(html_string, True)
    resource_expected = {
        "template_type": "html",
        "orientation": "landscape",
        "html_template_content": html_string,
    }
    assert resource.template_dict == resource_expected


def run():
    test_resource_base64()
    test_resource_raw()
    test_resource_local_file()
    test_resource_server_path()
    test_resource_url()
    test_resource_html()


if __name__ == "__main__":
    run()
