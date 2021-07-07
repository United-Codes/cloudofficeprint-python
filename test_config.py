import apexofficeprint as aop

from test import server

def test_pdf_options():
    """Test class PDFOptions in combination with OutputConfig"""
    pdf_opts = aop.config.PDFOptions(
        read_password='test_pw',
        watermark='test_watermark',
        page_width=500,
        page_height=500,
        even_page=True,
        merge_making_even=False,
        modify_password='test_modify_password',
        password_protection_flag=0,
        lock_form=True,
        copies=3,
        page_margin=5,
        landscape=False,
        page_format='test_page_format',
        merge=False,
        sign_certificate='test_sign_certificate',
        identify_form_fields=True)
    pdf_opts.set_page_margin_at(6, 'top')
    conf = aop.config.OutputConfig(filetype='pdf', pdf_options=pdf_opts)
    conf_expected = {
        'output_type': 'pdf',
        'output_encoding': 'raw',
        'output_converter': 'libreoffice',
        'output_read_password': 'test_pw',
        'output_watermark': 'test_watermark',
        'output_page_width': 500,
        'output_page_height': 500,
        'output_even_page': True,
        'output_merge_making_even': False,
        'output_modify_password': 'test_modify_password',
        'output_password_protection_flag': 0,
        'lock_form': True,
        'output_copies': 3,
        'page_margin': {
            'top': 6,
            'bottom': 5,
            'left': 5,
            'right': 5
        },
        'page_orientation': 'portrait',
        'output_page_format': 'test_page_format',
        'output_merge': False,
        'output_sign_certificate': 'test_sign_certificate',
        'identify_form_fields': True
    }
    assert conf.as_dict == conf_expected


def test_cloud_access_tokens():
    """Test cloud access for output file: OAuthToken, AWSToken, FTPToken and SFTPToken"""
    # OAuthToken
    o_auth_token = aop.config.CloudAccessToken.from_OAuth('dropbox', 'dummy_token')
    o_auth_token_expected = {
        'output_location': 'dropbox',
        'cloud_access_token': 'dummy_token'
    }
    assert o_auth_token.as_dict == o_auth_token_expected

    # AWSToken
    aws_token = aop.config.CloudAccessToken.from_AWS('AWS_access_key_id', 'AWS_secter_access_key')
    aws_token_expected = {
        "output_location": 'aws_s3',
        "cloud_access_token": {
            "access_key": 'AWS_access_key_id',
            "secret_access_key": 'AWS_secter_access_key'
        }
    }
    assert aws_token.as_dict == aws_token_expected

    # FTPToken & SFTPToken
    ftp_token = aop.config.CloudAccessToken.from_FTP('host_name', 35, 'dummy_user', 'dummy_pw')
    ftp_cloud_access_token = {
        'host': 'host_name',
        'port': 35,
        'user': 'dummy_user',
        'password': 'dummy_pw'
    }
    ftp_token_expected = {
        "output_location": 'ftp',
        "cloud_access_token": ftp_cloud_access_token
    }
    sftp_token = aop.config.CloudAccessToken.from_SFTP('host_name', 35, 'dummy_user', 'dummy_pw')
    sftp_token_expected = {
        "output_location": 'sftp',
        "cloud_access_token": ftp_cloud_access_token
    }
    assert ftp_token.as_dict == ftp_token_expected
    assert sftp_token.as_dict == sftp_token_expected


def test_commands():
    """Test post-process, conversion and merge commands"""
    # post_process
    post_process_command = aop.config.server.Command(
        command='echo_post',
        parameters={ "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
    )
    post_process_commands = aop.config.server.Commands(
        post_process=post_process_command,
        post_process_return=False,
        post_process_delete_delay=1500
    )
    post_process_expected = {
        "post_process": {
            "command": "echo_post",
            "return_output": False,
            "delete_delay": 1500,
            "command_parameters": { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
        }
    }
    assert post_process_commands._dict == post_process_expected

    # conversion
    pre_conversion_command = aop.config.server.Command(
        command='echo_pre',
        parameters={ "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
    )
    post_conversion_command = aop.config.server.Command(
        command='echo_post',
        parameters={ "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
    )
    conversion_commands = aop.config.server.Commands(
        pre_conversion=pre_conversion_command,
        post_conversion=post_conversion_command
    )
    conversion_expected = {
        'conversion': {
            'pre_command': 'echo_pre',
            'pre_command_parameters': { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" },
            'post_command': 'echo_post',
            'post_command_parameters': { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
        }
    }
    assert conversion_commands._dict == conversion_expected

    # merge
    post_merge_command = aop.config.server.Command(
        command='echo_post',
        parameters={ "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
    )
    post_merge_commands = aop.config.server.Commands(
        post_merge=post_merge_command
    )
    post_merge_expected = {
        'merge': {
            'post_command': 'echo_post',
            'post_command_parameters': { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
        }
    }
    assert post_merge_commands._dict == post_merge_expected


def test_route_paths():
    """Test output types of route path functions"""
    assert type(server.get_version_soffice()) == str
    assert type(server.get_version_officetopdf()) == str
    assert type(server.get_version_aop()) == str
    assert type(server.get_supported_template_mimetypes()) == dict
    assert type(server.get_supported_output_mimetypes('docx')) == dict
    assert type(server.get_supported_prepend_mimetypes()) == dict
    assert type(server.get_supported_append_mimetypes()) == dict


def run():
    test_pdf_options()
    test_cloud_access_tokens()
    test_commands()
    test_route_paths()
