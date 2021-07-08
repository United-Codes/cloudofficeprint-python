import apexofficeprint as aop
import asyncio
import pprint


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
    printjob_expected = {
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
        ],
        'python_sdk_version': aop.printjob.STATIC_OPTS['python_sdk_version']
    }
    assert printjob.as_dict == printjob_expected
    # printjob.execute().to_file("./test/prepend_append_subtemplate_test") # Works as expected


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
    pdf_texts_expected = {
        'AOP_PDF_TEXTS': [
            {
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
                '5': [
                    {
                        'text': 'test2',
                        'x': 60,
                        'y': 70,
                        'rotation': 30,
                        'bold': True,
                        'italic': True,
                        'font': 'Times new roman',
                        'font_color': '#FF00FF',
                        'font_size': 15
                    }
                ],
                'all': [
                    {
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
                ]
            }
        ]
    }
    assert pdf_texts.as_dict == pdf_texts_expected

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
    pdf_images_expected = {
        'AOP_PDF_IMAGES': [
            {
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
                '5': [
                    {
                        'image': 'test2',
                        'x': 20,
                        'y': 30,
                        'rotation': 15,
                        'image_width': 100,
                        'image_height': 100,
                        'image_max_width': 100
                    },
                ],
                'all': [
                    {
                        'image': 'test_all',
                        'x': 25,
                        'y': 26,
                        'rotation': 45,
                        'image_width': 20,
                        'image_height': 20,
                        'image_max_width': 50
                    }
                ]
            }
        ]
    }
    assert pdf_images.as_dict == pdf_images_expected


def test_aop_pdf_forms():
    form = aop.elements.PDFFormData(
        {
            'f_1': 5,
            'f_2': 'test',
            'r_1': True,
            'r_2': False
        }
    )
    form_expected = {
        'aop_pdf_form_data': {
            'f_1': 5,
            'f_2': 'test',
            'r_1': True,
            'r_2': False
        }
    }
    assert form.as_dict == form_expected


if __name__ == "__main__":
    # test1()
    # test_full_json()
    # asyncio.run(test_async())
    # test_chart()
    # test_aopchart()
    test_prepend_append_subtemplate()
    test_aop_pdf_texts()
    test_aop_pdf_images()
    test_aop_pdf_forms()

    from test_charts import run as test_charts
    test_charts()
    from test_config import run as test_config
    test_config()
    from test_codes import run as test_codes
    test_codes()
    from test_rest_source import run as test_rest_source
    test_rest_source()
    from test_resource import run as test_resource
    test_resource()
