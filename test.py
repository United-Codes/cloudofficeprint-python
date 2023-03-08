import cloudofficeprint as cop

###
#   Main file to run all the tests in the 'tests'-folder.
#   To run the tests:
#       1. Open the terminal in the parent directory
#       2. Type: python test.py
#       3. All tests succeeded if nothing is printed in the terminal
###

TEMPLATE_PATH = "./tests/data/template.docx"
SERVER_URL = "https://api.cloudofficeprint.com/"
API_KEY = "YOUR_API_KEY"  # Replace by your own API key
# NOTE: the API_KEY for this server object is only needed when running the functions `test_async()` and `test_full_json()`.
#   The other tests check if the generated JSON is as expected.

# Add server
server = cop.config.Server(SERVER_URL, cop.config.ServerConfig(api_key=API_KEY))


async def test_async():
    """Test if asynchronous execution succeeds."""
    # load a local file
    template = cop.Resource.from_local_file(TEMPLATE_PATH)

    data1 = cop.elements.ElementCollection()
    imageElement = cop.elements.Image.from_file("imageTag", "./tests/data/test.jpg")
    imageElement.max_width = 500
    imageElement.rotation = 75
    data1.add(imageElement)

    data2 = cop.elements.ElementCollection()
    data2.add(
        cop.elements.ElementCollection.from_mapping(
            {
                "textTag1": "Hello",
                "textTag2": ", ",
                "textTag3": "world",
                "textTag4": "!",
            }
        )
    )

    # create a print job with default output config
    printjob = cop.PrintJob({"output1": data1, "output2": data2}, server, template)

    try:
        coroutine = printjob.execute_async()
        print("Success?")
        res = await coroutine
        print("Success!")
        res.to_file("./tests/data/output")
    except cop.exceptions.COPError as err:
        print("Cloud Office Print error occurred! Encoded message below:")
        print(err.encoded_message)


def test_full_json():
    json_file = open("./tests/data/full_test.json", "r")
    json_data = json_file.read()
    cop.PrintJob.execute_full_json(json_data, server).to_file(
        "./tests/data/from_full_json_output"
    )


if __name__ == "__main__":
    # These two tests are commented out by default because they take longer than the others,
    #   because they send the template and data to a Cloud Office Print server and then save its response.
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
    from tests.test_template import run as test_template

    test_template()
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
