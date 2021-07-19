import apexofficeprint as aop
import asyncio

###
#   Main file to run all the tests in the 'tests'-folder.
#   To run the tests:
#       1. Open the terminal in the parent directory
#       2. Type: python test.py
#       3. All tests succeeded if nothing is printed in the terminal
###

TEMPLATE_PATH = "./tests/data/template.docx"
SERVER_URL = "http://apexofficeprint.com/dev/"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

# Add server
server = aop.config.Server(
    SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)

async def test_async():
    """Test if asynchronous execution succeeds."""
    # load a local file
    template = aop.Resource.from_local_file(TEMPLATE_PATH)

    data1 = aop.elements.ElementCollection()
    imageElement = aop.elements.Image.from_file("imageTag", "./tests/data/test.jpg")
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
        res.to_file("./tests/data/output")
    except aop.exceptions.AOPError as err:
        print("AOP error occurred! Encoded message below:")
        print(err.encoded_message)


def test_full_json():
    json_file = open("./tests/data/full_test.json", "r")
    json_data = json_file.read()
    aop.PrintJob.execute_full_json(json_data, server).to_file("./tests/data/from_full_json_output")


if __name__ == "__main__":
    # These two tests are commented out by default because they take longer than the others,
    #   because they send the template and data to an AOP server and then save its response.
    # asyncio.run(test_async())  # Works as expected
    # test_full_json()  # Works as expected


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
