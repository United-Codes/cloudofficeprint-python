from apexofficeprint._utils import file_utils
import apexofficeprint as aop
import asyncio
import pathlib
import pprint

from test_charts import run as test_charts_run


TEMPLATE_PATH = "./test/template.docx"
LOCAL_SERVER_URL = "http://localhost:8010"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

# Add server
server = aop.config.Server(
    LOCAL_SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)

def test_chart():
    line = aop.elements.LineChart(
        "chart-name",
        aop.elements.LineSeries([1, 2, 3, 4], [1, 2, 3, 4], color="green"),
        aop.elements.XYSeries([1, 2, 3, 4], ["a", "b", "c", "d"])
    )
    area = aop.elements.AreaChart(
        "area-chart-name", aop.elements.AreaSeries([1, 2, 3, 4], [5, 4, 6, 3]))
    combi = aop.elements.CombinedChart("combi-chart-name", [line], [area])
    del combi # del to avoid annoying unused var warning, thanks VS Code


def test_aopchart():
    aopchart = aop.elements.AOPChart(
        "chartName",
        [1, 2, 3, 4],
        [[5, 6, 8, 9], [3, 3, 3, 3]]
    )
    del aopchart


def test1():
    # load a local file
    template = aop.Resource.from_local_file(TEMPLATE_PATH)

    data1 = aop.elements.Object("data1")
    imageElement = aop.elements.Image.from_file("imageTag", "./test/test.jpg")
    imageElement.max_width = 500
    imageElement.rotation = 75
    data1.add(imageElement)

    data2 = aop.elements.Object("data2")
    data2.add_all(aop.elements.Object.from_mapping({
        "textTag1": "Hello",
        "textTag2": ", ",
        "textTag3": "world",
        "textTag4": "!"
    }))

    data3 = aop.elements.Object("nested_test", [data1, data2])
    data3_obj = aop.elements.Object.element_to_object(data3, "newObjName")
    del data3_obj

    # create a print job with default output config
    printjob = aop.PrintJob(template, {
        "output1": data1,
        "output2": data2
    }, server)

    try:
        res = printjob.execute()
        print("Success!")
        res.to_file("./test/output")
    except aop.exceptions.AOPError as err:
        print("AOP error occurred! Encoded message below:")
        print(err.encoded_message)


async def test_async():
    # load a local file
    template = aop.Resource.from_local_file(TEMPLATE_PATH)

    data1 = aop.elements.Object()
    imageElement = aop.elements.Image.from_file("imageTag", "./test/test.jpg")
    imageElement.max_width = 500
    imageElement.rotation = 75
    data1.add(imageElement)

    data2 = aop.elements.Object()
    data2.add(aop.elements.Object.from_mapping({
        "textTag1": "Hello",
        "textTag2": ", ",
        "textTag3": "world",
        "textTag4": "!"
    }))

    # create a print job with default output config
    printjob = aop.PrintJob(template, {
        "output1": data1,
        "output2": data2
    }, server)

    try:
        coroutine = printjob.execute_async()
        print("Success?")
        res = await coroutine
        print("Success!")
        res.to_file("./test/output")
    except aop.exceptions.AOPError as err:
        print("AOP error occurred! Encoded message below:")
        print(err.encoded_message)


def test_full_json():
    json_file = open("./test/full_test.json", "r")
    json_data = json_file.read()
    aop.PrintJob.execute_full_json(json_data, server).to_file("./test/from_full_json_output")

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
    conf_result = {
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
    assert conf.as_dict == conf_result

def test_cloud_access_tokens():
    """Test cloud access for output file: OAuthToken, AWSToken, FTPToken and SFTPToken"""
    # OAuthToken
    o_auth_token = aop.config.CloudAccessToken.from_OAuth('dropbox', 'dummy_token')
    o_auth_token_result = {
        'output_location': 'dropbox',
        'cloud_access_token': 'dummy_token'
    }
    assert o_auth_token.as_dict == o_auth_token_result

    # AWSToken
    aws_token = aop.config.CloudAccessToken.from_AWS('AWS_access_key_id', 'AWS_secter_access_key')
    aws_token_result = {
        "output_location": 'aws_s3',
        "cloud_access_token": {
            "access_key": 'AWS_access_key_id',
            "secret_access_key": 'AWS_secter_access_key'
        }
    }
    assert aws_token.as_dict == aws_token_result

    # FTPToken & SFTPToken
    ftp_token = aop.config.CloudAccessToken.from_FTP('host_name', 35, 'dummy_user', 'dummy_pw')
    ftp_cloud_access_token = {
        'host': 'host_name',
        'port': 35,
        'user': 'dummy_user',
        'password': 'dummy_pw'
    }
    ftp_token_result = {
        "output_location": 'ftp',
        "cloud_access_token": ftp_cloud_access_token
    }
    sftp_token = aop.config.CloudAccessToken.from_SFTP('host_name', 35, 'dummy_user', 'dummy_pw')
    sftp_token_result = {
        "output_location": 'sftp',
        "cloud_access_token": ftp_cloud_access_token
    }
    assert ftp_token.as_dict == ftp_token_result
    assert sftp_token.as_dict == sftp_token_result

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
    post_process_result = {
        "post_process": {
            "command": "echo_post",
            "return_output": False,
            "delete_delay": 1500,
            "command_parameters": { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
        }
    }
    assert post_process_commands._dict == post_process_result

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
    conversion_result = {
        'conversion': {
            'pre_command': 'echo_pre',
            'pre_command_parameters': { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" },
            'post_command': 'echo_post',
            'post_command_parameters': { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
        }
    }
    assert conversion_commands._dict == conversion_result

    # merge
    post_merge_command = aop.config.server.Command(
        command='echo_post',
        parameters={ "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
    )
    post_merge_commands = aop.config.server.Commands(
        post_merge=post_merge_command
    )
    post_merge_result = {
        'merge': {
            'post_command': 'echo_post',
            'post_command_parameters': { "p1":"Parameter1", "p2": "Parameter2" , "p3": "Parameter3" }
        }
    }
    assert post_merge_commands._dict == post_merge_result

def test_resource():
    """Test if the different types of resources return the expected result."""
    # Base64
    resource = aop.Resource.from_base64('dummy', 'docx')
    resource_result = {
        'file': 'dummy',
        'template_type': 'docx'
    }
    assert resource.template_dict == resource_result

    # Local file (raw)
    local_path = str(pathlib.Path().resolve()) + '/test/template.docx'
    resource = aop.Resource.from_local_file(local_path)
    with open(local_path, "rb") as f:
        content = f.read()
    resource_result = {
        'file': file_utils.raw_to_base64(content),
        'template_type': 'docx'
    }
    assert resource.template_dict == resource_result

    # Server path
    resource = aop.Resource.from_server_path('dummy/path.docx')
    resource_result = {
        'filename': 'dummy/path.docx',
        'template_type': 'docx'
    }
    assert resource.template_dict == resource_result

    # URL
    resource = aop.Resource.from_url('dummy_url', 'docx')
    resource_result = {
        'template_type': 'docx',
        'url': 'dummy_url'
    }
    assert resource.template_dict == resource_result

    # HTML
    html_string = """
     <!DOCTYPE html>
    <html>
    <body>

    <h1>My First Heading</h1>
    <p>My first paragraph.</p>

    </body>
    </html> 
    """
    resource = aop.Resource.from_html(html_string, True)
    resource_result = {
        'template_type': 'html',
        'orientation': 'landscape',
        'html_template_content': html_string
    }
    assert resource.template_dict == resource_result

def test_prepend_append_subtemplate():
    """Test prepending and appending files in class Printjob"""
    prepend_file = aop.Resource.from_local_file('./test/template.docx')

    template = aop.Resource.from_local_file('./test/template.docx')
    template_main = aop.Resource.from_local_file('./test/template_prepend_append_subtemplate.docx')
    template_base64 = template.base64
    template_main_base64 = template_main.base64
    
    data = aop.elements.Object('data')
    text_tag = aop.elements.Property('textTag1', 'test_text_tag1')
    data.add(text_tag)

    append_file = aop.Resource.from_local_file('./test/template.docx')

    subtemplates = {
        'sub1': template,
        'sub2': template
    }

    output_conf = aop.config.OutputConfig(filetype='pdf')

    printjob = aop.PrintJob(template=template_main,
        data=data,
        server=server,
        output_config=output_conf,
        subtemplates=subtemplates,
        prepend_files=[prepend_file],
        append_files=[append_file])
    printjob_result = {
        'api_key': API_KEY,
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
        ]
        }
    assert printjob.as_dict == printjob_result
    # printjob.execute().to_file("./test/prepend_append_subtemplate_test") # Works as expected

def test_route_paths():
    """Test output types of route path functions"""
    assert type(server.get_version_soffice()) == str
    assert type(server.get_version_officetopdf()) == str
    assert type(server.get_version_aop()) == str
    assert type(server.get_supported_template_mimetypes()) == dict
    assert type(server.get_supported_output_mimetypes('docx')) == dict
    assert type(server.get_supported_prepend_mimetypes()) == dict
    assert type(server.get_supported_append_mimetypes()) == dict

def test_aop_pdf_texts():
    """Test aop_pdf_texts element"""
    pdf_text1_1 = aop.elements.PDFText(
        text='test1_1',
        x=50,
        y=60,
        page=3,
        rotation=45,
        bold=False,
        italic=True,
        font='Arial',
        font_color='blue',
        font_size=12
    )
    pdf_text1_2 = aop.elements.PDFText(
        text='test1_2',
        x=20,
        y=30,
        page=3,
        rotation=45,
        bold=False,
        italic=False,
        font='Arial',
        font_color='red',
        font_size=10
    )
    pdf_text2 = aop.elements.PDFText(
        text='test2',
        x=60,
        y=70,
        page=5,
        rotation=30,
        bold=True,
        italic=True,
        font='Times new roman',
        font_color='#FF00FF',
        font_size=15
    )
    pdf_text_all = aop.elements.PDFText(
        text='test_all',
        x=20,
        y=30,
        rotation=15,
        bold=True,
        italic=False,
        font='Arial',
        font_color='red',
        font_size=20
    )
    pdf_texts = aop.elements.PDFTexts((pdf_text1_1, pdf_text1_2, pdf_text2, pdf_text_all))
    pdf_texts_results = {
        '3': [
            {
                'text': 'test1_1',
                'x': 50,
                'y': 60,
                'rotation': 45,
                'bold': False,
                'italic': True,
                'font': 'Arial',
                'font_color': 'blue',
                'font_size': 12
            },
            {
                'text': 'test1_2',
                'x': 20,
                'y': 30,
                'rotation': 45,
                'bold': False,
                'italic': False,
                'font': 'Arial',
                'font_color': 'red',
                'font_size': 10
            }
        ],
        '5': {
            'text': 'test2',
            'x': 60,
            'y': 70,
            'rotation': 30,
            'bold': True,
            'italic': True,
            'font': 'Times new roman',
            'font_color': '#FF00FF',
            'font_size': 15
        },
        'all': {
            'text': 'test_all',
            'x': 20,
            'y': 30,
            'rotation': 15,
            'bold': True,
            'italic': False,
            'font': 'Arial',
            'font_color': 'red',
            'font_size': 20
        }
    }
    assert pdf_texts.as_dict == pdf_texts_results

def test_aop_pdf_images():
    """Test aop_pdf_images element"""
    pdf_image1_1 = aop.elements.PDFImage(
        image='test1_1',
        x=50,
        y=60,
        page=3,
        rotation=45,
        width=50,
        height=50,
        max_width=100
    )
    pdf_image1_2 = aop.elements.PDFImage(
        image='test1_2',
        x=60,
        y=70,
        page=3,
        rotation=30,
        width=75,
        height=75,
        max_width=75
    )
    pdf_image2 = aop.elements.PDFImage(
        image='test2',
        x=20,
        y=30,
        page=5,
        rotation=15,
        width=100,
        height=100,
        max_width=100
    )
    pdf_image_all = aop.elements.PDFImage(
        image='test_all',
        x=25,
        y=26,
        rotation=45,
        width=20,
        height=20,
        max_width=50
    )
    pdf_images = aop.elements.PDFImages((pdf_image1_1, pdf_image1_2, pdf_image2, pdf_image_all))
    pdf_images_result = {
        '3': [
            {
                'image': 'test1_1',
                'x': 50,
                'y': 60,
                'rotation': 45,
                'image_width': 50,
                'image_height': 50,
                'image_max_width': 100
            },
            {
                'image': 'test1_2',
                'x': 60,
                'y': 70,
                'rotation': 30,
                'image_width': 75,
                'image_height': 75,
                'image_max_width': 75
            }
        ],
        '5': {
            'image': 'test2',
            'x': 20,
            'y': 30,
            'rotation': 15,
            'image_width': 100,
            'image_height': 100,
            'image_max_width': 100
        },
        'all': {
            'image': 'test_all',
            'x': 25,
            'y': 26,
            'rotation': 45,
            'image_width': 20,
            'image_height': 20,
            'image_max_width': 50
        }
    }
    assert pdf_images.as_dict == pdf_images_result

def test_barcodes():
    """Test class BarCode, a subclass of class Code"""
    barcode = aop.elements.BarCode(
        name='name',
        data='data',
        type='ean13',
        height=50,
        width=50,
        errorcorrectlevel='L',
        url='url',
        rotation=45,
        background_color='red',
        padding_width=25,
        padding_height=25,
        extra_options='includetext guardwhitespace'
    )
    barcode_result = {
        'name': 'data',
        'name_type': 'ean13',
        'name_height': 50,
        'name_width': 50,
        'name_errorcorrectlevel': 'L',
        'name_url': 'url',
        'name_rotation': 45,
        'name_background_color': 'red',
        'name_padding_width': 25,
        'name_padding_height': 25,
        'name_extra_options': 'includetext guardwhitespace'
    }
    assert barcode.as_dict == barcode_result

def test_qr_codes():
    """Test class QRCode, a subclass of class Code, and all its subclasses"""
    wifi = aop.elements.WiFiQRCode(
        name='name',
        ssid='ssid',
        wifi_password='password',
        wifi_encryption='WPA',
        wifi_hidden=False
    )
    wifi_result = {
        'name': 'ssid',
        'name_type': 'qr_wifi',
        'name_wifi_password': 'password',
        'name_wifi_encryption': 'WPA',
        'name_wifi_hidden': False
    }
    assert wifi.as_dict == wifi_result

    telephone_number = aop.elements.TelephoneNumberQRCode(
        name='name',
        number='+32_test_number'
    )
    telephone_number_result = {
        'name': '+32_test_number',
        'name_type': 'qr_telephone'
    }
    assert telephone_number.as_dict == telephone_number_result

    email = aop.elements.EmailQRCode(
        name='name',
        receiver='receiver',
        cc='cc',
        bcc='bcc',
        subject='subject',
        body='body'
    )
    email_result = {
        'name': 'receiver',
        'name_type': 'qr_email',
        'name_email_cc': 'cc',
        'name_email_bcc': 'bcc',
        'name_email_subject': 'subject',
        'name_email_body': 'body'
    }
    assert email.as_dict == email_result

    sms = aop.elements.SMSQRCode(
        name='name',
        receiver='receiver',
        sms_body='sms_body'
    )
    sms_result = {
        'name': 'receiver',
        'name_type': 'qr_sms',
        'name_sms_body': 'sms_body'
    }
    assert sms.as_dict == sms_result

    url = aop.elements.URLQRCode(
        name='name',
        url='url'
    )
    url_result = {
        'name': 'url',
        'name_type': 'qr_url'
    }
    assert url.as_dict == url_result

    v_card = aop.elements.VCardQRCode(
        name='name',
        first_name='first_name',
        last_name='last_name',
        email='email',
        website='website'
    )
    v_card_result = {
        'name': 'first_name',
        'name_type': 'qr_vcard',
        'name_vcard_last_name': 'last_name',
        'name_vcard_email': 'email',
        'name_vcard_website': 'website'
    }
    assert v_card.as_dict == v_card_result

    me_card = aop.elements.MeCard(
        name='name',
        first_name='first_name',
        last_name='last_name',
        nickname='nickname',
        email='email',
        contact_primary='contact_primary',
        contact_secondary='contact_secondary',
        contact_tertiary='contact_tertiary',
        website='website',
        birthday='birthday',
        notes='notes'
    )
    me_card_result = {
        'name': 'first_name',
        'name_type': 'qr_me_card',
        'name_me_card_last_name': 'last_name',
        'name_me_card_nickname': 'nickname',
        'name_me_card_email': 'email',
        'name_me_card_contact_primary': 'contact_primary',
        'name_me_card_contact_secondary': 'contact_secondary',
        'name_me_card_contact_tertiary': 'contact_tertiary',
        'name_me_card_website': 'website',
        'name_me_card_birthday': 'birthday',
        'name_me_card_notes': 'notes'
    }
    assert me_card.as_dict == me_card_result

    geolocation = aop.elements.GeolocationQRCode(
        name='name',
        latitude='latitude',
        longitude='longitude',
        altitude='altitude'
    )
    geolocation_result = {
        'name': 'latitude',
        'name_type': 'qr_geolocation',
        'name_geolocation_longitude': 'longitude',
        'name_geolocation_altitude': 'altitude'
    }
    assert geolocation.as_dict == geolocation_result

    event = aop.elements.EventQRCode(
        name='name',
        summary='summary',
        startdate='startdate',
        enddate='enddate'
    )
    event_result = {
        'name': 'summary',
        'name_type': 'qr_event',
        'name_event_startdate': 'startdate',
        'name_event_enddate': 'enddate'
    }
    assert event.as_dict == event_result
    

if __name__ == "__main__":
    # test1()
    # test_full_json()
    # asyncio.run(test_async())
    # test_chart()
    # test_aopchart()
    test_pdf_options()
    test_cloud_access_tokens()
    test_commands()
    test_resource()
    test_prepend_append_subtemplate()
    test_route_paths()
    test_aop_pdf_texts()
    test_aop_pdf_images()
    test_barcodes()
    test_qr_codes()

    # Test charts (from test_charts.py)
    test_charts_run()
