# About
There is a limit on how much data can be sent to an AOP server at once. Let's say you have a template for product specifications and you want to generate one merged PDF file for 50.000 different products. It is possible that you cannot send all the data for all the products at once to the AOP server. In this example we will show you how you can split one big merge request into multiple smaller merge requests.

# Template
A simple template will be used since the goal of this example is to show how you can split one big merge request into a few smaller ones. The template will contain one simple tag {test}. Tags are used in a template to let the AOP server know what needs to be replaced by data. In this case, the simple tag {test} will be replaced by whatever value is given to the AOP server for the tag with key 'test'. In this example we use a template with filetype docx, but this can be any of the allowed template types (see [here](https://www.apexofficeprint.com/docs/#tag-overview)).

<img src="./template.png" width="600" />
<!-- TODO: change this link to Github link -->

# Code (SDK)
First we create a new file and import the APEX Office Print library:
```python
import apexofficeprint as aop
```

Then we need to set up the AOP server where we will send our template and data to:
```python
SERVER_URL = "https://api.apexofficeprint.com/"
API_KEY = "YOUR_API_KEY"  # Replace by your own API key

server = aop.config.Server(
    SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)
```
If you have an AOP server running on localhost (e.g. on-premise version), replace the server url by the localhost url: http://localhost:8010

We also need to create the main element-collection object that contains all our data. Let's say we have 100 different customers for who we need to fill in the template and we want to merge the resulting files into a PDF. In this example, we are just going to repeat the property 'test' with value 'test' 100 times, but normally you would have different data for each customer.
```python
data = {
    'file'+str(i): aop.elements.Property('test', 'test') for i in range(100)
}
```


We want the output PDF files to be merged, so we create an output configuration:
```python
conf = aop.config.OutputConfig(
    filetype='pdf',
    pdf_options=aop.config.PDFOptions(
        merge=True
    )
)
```


Let's assume that the AOP server can't handle all the data at once, so we need to split our data into multiple requests. Let's use 10 requests with each 10 elements in the data (a total of 100 data elements).
```python
output_files: List[aop.Response] = []
for i in range(10):
    # Create print job with 10 data elements
    printjob = aop.PrintJob(
        data={
            k[0]: k[1] for k in list(data.items())[i*10: (i+1)*10] # Select 10 data elements from the data
        },
        server=server,
        template=aop.Resource.from_local_file('./output'),
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
        aop.Resource.from_raw(
            raw_data=response.binary,
            filetype='pdf'
        )
    )
```

Finally, we create the print job for the last request that merges the 10 merged PDF's. As the template we pick the first PDF in the resources-list and the other 9 PDFs from the resources-list can be added as files that need to be appended to the template file.
```python
printjob = aop.PrintJob(
    data=aop.elements.Property('not_used', 'not_used'),
    server=server,
    template=resources[0],
    append_files=resources[1:]
)
printjob.execute().to_file('./output')
```
