import pathlib

import cloudofficeprint as cop


def test_template_base64():
    template = cop.Template.from_base64("dummy", "docx")
    template_expected = {
        "file": "dummy",
        "template_type": "docx",
    }
    assert template.template_dict == template_expected


def test_template_local_file():
    local_path = str(pathlib.Path().resolve()) + "/tests/data/template.docx"
    with open(local_path, "rb") as f:
        data = f.read()
    template = cop.Template.from_local_file(local_path)
    template_expected = {
        "file": cop.own_utils.raw_to_base64(data),
        "template_type": "docx",
    }
    assert template.template_dict == template_expected


def test_template_delimiters():
    template = cop.Template.from_base64("dummy", "docx", "<", ">")
    template_expected = {
        "file": "dummy",
        "template_type": "docx",
        "start_delimiter": "<",
        "end_delimiter": ">",
    }
    assert template.template_dict == template_expected


def test_template_hashing():
    template = cop.Template.from_base64("dummy", "docx", "<", ">", True)
    template_expected = {
        "file": "dummy",
        "template_type": "docx",
        "should_hash": True,
        "start_delimiter": "<",
        "end_delimiter": ">",
    }
    assert template.template_dict == template_expected


def test_template_with_hash():
    template = cop.Template.from_base64("dummy", "docx", "<", ">", False, "test_hash")
    template_expected = {
        "template_hash": "test_hash",
        "template_type": "docx",
        "start_delimiter": "<",
        "end_delimiter": ">",
    }
    assert template.template_dict == template_expected


def test_template_updating_hash():
    template = cop.Template.from_base64("dummy", "docx", "<", ">", True)
    template.update_hash("test_hash")
    template_expected = {
        "template_type": "docx",
        "template_hash": "test_hash",
        "start_delimiter": "<",
        "end_delimiter": ">",
    }
    assert template.template_dict == template_expected


def test_template_resetting_hash():
    template = cop.Template.from_base64("dummy", "docx", "<", ">", False, "test_hash")
    template.reset_hash(True)
    template_expected = {
        "file": "dummy",
        "template_type": "docx",
        "should_hash": True,
        "start_delimiter": "<",
        "end_delimiter": ">",
    }
    assert template.template_dict == template_expected


def run():
    test_template_base64()
    test_template_local_file()
    test_template_delimiters()
    test_template_hashing()
    test_template_with_hash()
    test_template_updating_hash()
    test_template_resetting_hash()


if __name__ == "__main__":
    run()
