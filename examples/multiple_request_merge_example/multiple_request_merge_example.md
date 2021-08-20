# About
There is a limit on how much data can be sent to a Cloud Office Print server at once. Let's say you have a template for product specifications and you want to generate one merged PDF file for 50.000 different products. It is possible that you cannot send all the data for all the products at once to the Cloud Office Print server. In this example we will show you how you can split one big merge request into multiple smaller merge requests.

# Template
A simple template will be used since the goal of this example is to show how you can split one big merge request into a few smaller ones. The template will contain one simple tag {test}. Tags are used in a template as placeholders to let the Cloud Office Print server know what needs to be replaced by data. In this case, the simple tag {test} will be replaced by whatever value is given to the Cloud Office Print server for the tag with key 'test'. In this example we use a template with filetype docx, but this can be any of the allowed template types (see [here](https://www.cloudofficeprint.com/docs/#tag-overview)).

<img src="https://raw.githubusercontent.com/United-Codes/cloudofficeprint-python/master/examples/multiple_request_merge_example/template.png" width="600" />

# Code (SDK)
NOTE: For an overview of all the possibilities of this SDK, we refer to the documentation on our [website](https://cloudofficeprint.com/docs).
First we create a new file and import the Cloud Office Print library:
```python
import cloudofficeprint as cop
```

Then we need to set up the Cloud Office Print server where we will send our template and data to:
```python
SERVER_URL = "https://api.cloudofficeprint.com/"
API_KEY = "YOUR_API_KEY"  # Replace by your own API key

server = cop.config.Server(
    SERVER_URL,
    cop.config.ServerConfig(api_key=API_KEY)
)
```
If you have a Cloud Office Print server running on localhost (e.g. on-premise version), replace the server url by the localhost url: http://localhost:8010

We also need to create the main element-collection object that contains all our data. Let's say we have 100 different customers for who we need to fill in the template and we want to merge the resulting files into a PDF. In this example, we are just going to repeat the property 'test' with value 'test' 100 times, but normally you would have different data for each customer.
```python
data = {
    'file'+str(i): cop.elements.Property('test', 'test') for i in range(100)
}
```


We want the output PDF files to be merged, so we create an output configuration:
```python
conf = cop.config.OutputConfig(
    filetype='pdf',
    pdf_options=cop.config.PDFOptions(
        merge=True
    )
)
```


Let's assume that the Cloud Office Print server can't handle all the data at once, so we need to split our data into multiple requests. Let's use 10 requests with each 10 elements in the data (a total of 100 data elements).
```python
output_files: List[cop.Response] = []
for i in range(10):
    # Create print job with 10 data elements
    printjob = cop.PrintJob(
        data={
            k[0]: k[1] for k in list(data.items())[i*10: (i+1)*10] # Select 10 data elements from the data
        },
        server=server,
        template=cop.Resource.from_local_file('./examples/multiple_request_merge_example/template.docx'),
        output_config=conf
    )

    # Execute the print job and save the response to a list
    output_files.append(printjob.execute())
```


Now that we saved the server response for all the smaller tasks, we create the final request to merge all the received (merged) PDFs. Therefore we create Resource-objects from the Response-objects.
```python
resources = []
for response in output_files:
    resources.append(
        cop.Resource.from_raw(
            raw_data=response.binary,
            filetype='pdf'
        )
    )
```

Finally, we create the print job for the last request that merges the 10 merged PDF's. As the template we pick the first PDF in the resources-list and the other 9 PDFs from the resources-list can be added as files that need to be appended to the template file.
```python
printjob = cop.PrintJob(
    data=cop.elements.Property('not_used', 'not_used'),
    server=server,
    template=resources[0],
    append_files=resources[1:]
)
printjob.execute().to_file('./examples/multiple_request_merge_example/output')
```
