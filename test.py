import apexofficeprint as aop
import asyncio

TEMPLATE_PATH = "./test/template.docx"
LOCAL_SERVER_URL = "http://localhost:8010"
API_KEY = "1C511A58ECC73874E0530100007FD01A"


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
    server = aop.config.Server(
        LOCAL_SERVER_URL, aop.config.ServerConfig(api_key=API_KEY))
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
    server = aop.config.Server(
        LOCAL_SERVER_URL, aop.config.ServerConfig(api_key=API_KEY))
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
    server = aop.config.Server(
        LOCAL_SERVER_URL,
        aop.config.ServerConfig(api_key=API_KEY)
    )
    json_file = open("./test/full_test.json", "r")
    json_data = json_file.read()
    aop.PrintJob.execute_full_json(json_data, server).to_file("./test/from_full_json_output")

def test_pdf_options():
    pdf_opts = aop.config.PDFOptions(read_password='test_pw', landscape=False)
    conf = aop.config.OutputConfig(filetype='pdf', pdf_options=pdf_opts)
    conf_result = {
        'output_type': 'pdf',
        'output_encoding': 'raw',
        'output_converter': 'libreoffice',
        'output_read_password': 'test_pw',
        'output_page_orientation': 'portrait'
    }
    assert conf.as_dict == conf_result

def test_cloud_access_tokens():
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


if __name__ == "__main__":
    # test1()
    # test_full_json()
    # asyncio.run(test_async())
    # test_chart()
    # test_aopchart()
    test_pdf_options()
    test_cloud_access_tokens()
    test_commands()
    # pass
