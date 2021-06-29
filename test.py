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


if __name__ == "__main__":
    # test1()
    # test_full_json()
    # asyncio.run(test_async())
    # test_chart()
    # test_aopchart()
    pass
