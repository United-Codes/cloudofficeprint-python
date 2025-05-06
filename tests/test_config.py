import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop


def test_pdf_options():
    """Test class PDFOptions in combination with OutputConfig"""
    
    pdf_opts = cop.config.PDFOptions(
        even_page=True,
        merge_making_even=False,
        remove_last_page=False,
        modify_password="test_modify_password",
        read_password="test_pw",
        password_protection_flag=0,
        watermark="test_watermark",
        watermark_color="black",
        watermark_font="Arial",
        watermark_opacity=50,
        watermark_font_size=32,
        lock_form=True,
        copies=3,
        page_margin=5,
        landscape=True,
        page_width=500,
        page_height=500,
        page_format="test_page_format",
        merge=False,
        split=True,
        identify_form_fields=True,
        sign_certificate="test_sign_certificate",
        sign_certificate_password="test_certificate_password",
        sign_certificate_txt="text in english",
        convert_to_pdfa = "1b",
        convert_attachment_to_json= True,
        insert_barcode= True,
    )
    pdf_opts.set_watermark("new_watermark", "grey", "Arial", 51, 32, 45)
    pdf_opts.set_page_margin_at(6, "top")
    pdf_opts.page_orientation = "portrait"
    conf = cop.config.OutputConfig(filetype="pdf", converter="openoffice", update_toc=True, return_output=True, pdf_options=pdf_opts)
    conf_expected = {
        "output_even_page": True,
        "output_merge_making_even": False,
        "output_remove_last_page": False,
        "output_modify_password": "test_modify_password",
        "output_read_password": "test_pw",
        "output_password_protection_flag": 0,
        "output_watermark": "new_watermark",
        "output_watermark_color": "grey",
        "output_watermark_font": "Arial",
        "output_watermark_opacity": 51,
        "output_watermark_size": 32,
        "output_watermark_rotation": 45,
        "output_type": "pdf",
        "output_encoding": "raw",
        "output_converter": "openoffice",
        "update_toc": True,
        "return_output":True,
        "output_page_width": 500,
        "output_page_height": 500,
        "lock_form": True,
        "output_copies": 3,
        "page_margin": {
            "top": 6,
            "bottom": 5,
            "left": 5,
            "right": 5,
        },
        "page_orientation": "portrait",
        "output_page_format": "test_page_format",
        "output_merge": False,
        "output_sign_certificate": "test_sign_certificate",
        "output_sign_certificate_password": "test_certificate_password",
        "output_sign_certificate_txt": "text in english",
        "output_convert_to_pdfa": "1b",
        "output_convert_attachment_to_json": True,
        "output_insert_barcode": True,
        "identify_form_fields": True,
        "output_split": True,
    }
    assert conf.as_dict == conf_expected


def test_csv_options():
    csv_opts = cop.config.CsvOptions("text_delim", "field_sep", 5)
    csv_opts_expected = {
        "output_text_delimiter": "text_delim",
        "output_field_separator": "field_sep",
        "output_character_set": 5,
    }
    assert csv_opts.as_dict == csv_opts_expected


def test_printer():
    printer = cop.config.Printer(
        location='location',
        version='version',
        requester='requester',
        job_name='job_name',
        return_output=False
    )
    printer_expected = {
        'location': 'location',
        'version': 'version',
        'requester': 'requester',
        'job_name': 'job_name',
        'return_output': False
    }
    assert printer._dict == printer_expected


def test_cloud_access_tokens():
    """Test cloud access for output file: OAuthToken, AWSToken, FTPToken and SFTPToken"""
    # OAuthToken
    o_auth_token = cop.config.CloudAccessToken.from_OAuth("dropbox", "dummy_token")
    o_auth_token_expected = {
        "output_location": "dropbox",
        "cloud_access_token": "dummy_token",
    }
    assert o_auth_token.as_dict == o_auth_token_expected

    # AWSToken
    aws_token = cop.config.CloudAccessToken.from_AWS(
        "AWS_access_key_id", "AWS_secter_access_key"
    )
    aws_token_expected = {
        "output_location": "aws_s3",
        "cloud_access_token": {
            "access_key": "AWS_access_key_id",
            "secret_access_key": "AWS_secter_access_key",
        },
    }
    assert aws_token.as_dict == aws_token_expected

    # FTPToken & SFTPToken
    ftp_token = cop.config.CloudAccessToken.from_FTP(
        "host_name", 35, "dummy_user", "dummy_pw"
    )
    ftp_cloud_access_token = {
        "host": "host_name",
        "port": 35,
        "user": "dummy_user",
        "password": "dummy_pw",
    }
    ftp_token_expected = {
        "output_location": "ftp",
        "cloud_access_token": ftp_cloud_access_token,
    }
    sftp_token = cop.config.CloudAccessToken.from_SFTP(
        "host_name", 35, "dummy_user", "dummy_pw"
    )
    sftp_token_expected = {
        "output_location": "sftp",
        "cloud_access_token": ftp_cloud_access_token,
    }
    assert ftp_token.as_dict == ftp_token_expected
    assert sftp_token.as_dict == sftp_token_expected


def test_commands():
    """Test post-process, conversion and merge commands"""
    # post_process
    post_process_command = cop.config.Command(
        command="echo_post",
        parameters={"p1": "Parameter1", "p2": "Parameter2", "p3": "Parameter3"},
    )
    post_process_commands = cop.config.Commands(
        post_process=post_process_command,
        post_process_return=False,
        post_process_delete_delay=1500,
    )
    post_process_expected = {
        "post_process": {
            "command": "echo_post",
            "return_output": False,
            "delete_delay": 1500,
            "command_parameters": {
                "p1": "Parameter1",
                "p2": "Parameter2",
                "p3": "Parameter3",
            },
        }
    }
    assert post_process_commands._dict == post_process_expected

    # conversion
    pre_conversion_command = cop.config.Command(
        command="echo_pre",
        parameters={"p1": "Parameter1", "p2": "Parameter2", "p3": "Parameter3"},
    )
    post_conversion_command = cop.config.Command(
        command="echo_post",
        parameters={"p1": "Parameter1", "p2": "Parameter2", "p3": "Parameter3"},
    )
    conversion_commands = cop.config.Commands(
        pre_conversion=pre_conversion_command, post_conversion=post_conversion_command
    )
    conversion_expected = {
        "conversion": {
            "pre_command": "echo_pre",
            "pre_command_parameters": {
                "p1": "Parameter1",
                "p2": "Parameter2",
                "p3": "Parameter3",
            },
            "post_command": "echo_post",
            "post_command_parameters": {
                "p1": "Parameter1",
                "p2": "Parameter2",
                "p3": "Parameter3",
            },
        }
    }
    assert conversion_commands._dict == conversion_expected

    # merge
    post_merge_command = cop.config.Command(
        command="echo_post",
        parameters={"p1": "Parameter1", "p2": "Parameter2", "p3": "Parameter3"},
    )
    post_merge_commands = cop.config.Commands(post_merge=post_merge_command)
    post_merge_expected = {
        "merge": {
            "post_command": "echo_post",
            "post_command_parameters": {
                "p1": "Parameter1",
                "p2": "Parameter2",
                "p3": "Parameter3",
            },
        }
    }
    assert post_merge_commands._dict == post_merge_expected


def test_route_paths():
    """Test output types of route path functions"""
    server = cop.config.Server(
        "https://api.cloudofficeprint.com/", cop.config.ServerConfig("YOUR_API_KEY")
    )
    assert server.is_reachable() == True
    assert type(server.get_version_cop()) == str
    assert type(server.get_version_soffice()) == str
    assert type(server.get_version_officetopdf()) == str
    assert type(server.get_supported_template_mimetypes()) == dict
    assert type(server.get_supported_output_mimetypes("docx")) == dict
    assert type(server.get_supported_prepend_mimetypes()) == dict
    assert type(server.get_supported_append_mimetypes()) == dict
    # assert type(server.verify_template_hash("test_hash")) == dict
    # assert type(server.check_ipp("http://localhost:3000", "1.1")) == dict


def test_request_option():
    extra_headers = {
        "file_id": "Any file id like FILE_123",
        "access_token": "Access Token for above hostname (if any) "
    }
    request_opt = cop.config.request_option(
        "https://www.apexofficeprint.com/post/", extra_headers)
    config = cop.config.OutputConfig(
        filetype='pdf', output_polling=True, request_option=request_opt, secret_key='qwertyuiop1234')
    config_expected = {
        'output_type': 'pdf',
        'output_encoding': 'raw',
        'output_converter': 'libreoffice',
        'output_polling': 'True',
        'secret_key': 'qwertyuiop1234',
        'request_option': {
            'url': 'https://www.apexofficeprint.com/post/',
            'extra_headers': {
                'file_id': 'Any file id like FILE_123',
                'access_token': 'Access Token for above hostname (if any) '
            }
        }
    }
    assert config.as_dict == config_expected

def test_output_locale_option():
    """test output locale option"""
    config = cop.config.OutputConfig(output_locale='nepali')
    config_expected= {
        'output_locale': 'nepali',
        'output_encoding': 'raw',
        'output_converter': 'libreoffice',
    }
    assert config.as_dict == config_expected

def test_password_encryption():
    """test output_read_password option"""
    config = cop.config.OutputConfig(output_read_password="aop_pass")
    config_expected = {
        "output_read_password": "aop_pass",
        "output_encoding": "raw",
        "output_converter": "libreoffice",
    }
    assert config.as_dict == config_expected
    # print(config.as_dict)



def run():
    test_pdf_options()
    test_csv_options()
    test_printer()
    test_cloud_access_tokens()
    test_commands()
    test_route_paths()
    test_output_locale_option() 
    test_password_encryption()


if __name__ == "__main__":
    run()
