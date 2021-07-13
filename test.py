import apexofficeprint as aop
import asyncio
import pprint

###
#   Main file to run all the tests in the 'tests'-folder
###

TEMPLATE_PATH = "./test/template.docx"
LOCAL_SERVER_URL = "http://localhost:8010"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

# Add server
server = aop.config.Server(
    LOCAL_SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)

def test1():
    # load a local file
    template = aop.Resource.from_local_file(TEMPLATE_PATH)

    data1 = aop.elements.ElementCollection("data1")
    imageElement = aop.elements.Image.from_file("imageTag", "./test/test.jpg")
    imageElement.max_width = 500
    imageElement.rotation = 75
    data1.add(imageElement)

    data2 = aop.elements.ElementCollection("data2")
    data2.add_all(aop.elements.ElementCollection.from_mapping({
        "textTag1": "Hello",
        "textTag2": ", ",
        "textTag3": "world",
        "textTag4": "!"
    }))

    data3 = aop.elements.ElementCollection("nested_test", [data1, data2])
    data3_obj = aop.elements.ElementCollection.element_to_element_collection(data3, "newObjName")
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

    data1 = aop.elements.ElementCollection()
    imageElement = aop.elements.Image.from_file("imageTag", "./test/test.jpg")
    imageElement.max_width = 500
    imageElement.rotation = 75
    data1.add(imageElement)

    data2 = aop.elements.ElementCollection()
    data2.add(aop.elements.ElementCollection.from_mapping({
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


if __name__ == "__main__":
    # test1()
    # test_full_json()
    # asyncio.run(test_async())


    from tests.test_charts import run as test_charts
    test_charts()
    from tests.test_config import run as test_config
    test_config()
    from tests.test_codes import run as test_codes
    test_codes()
    from tests.test_rest_source import run as test_rest_source
    test_rest_source()
    from tests.test_resource import run as test_resource
    test_resource()
    from tests.test_printjob import run as test_printjob
    test_printjob()
    from tests.test_pdf import run as test_pdf
    test_pdf()
    from tests.test_loops import run as test_loops
    test_loops()
    from tests.test_images import run as test_images
    test_images()
    from tests.test_elements import run as test_elements
    test_elements()
