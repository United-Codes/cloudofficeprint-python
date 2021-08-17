"""This is an example of how you can merge the output files generated from a single template using multiple requests.
This approach is useful if you are dealing with a lot of output files that need to be merged.
There is a limit on how much data can be sent to a cloud Office Print server, so this is useful to split one big request into multiple smaller ones.
This example will take a minute to run.
"""

from typing import List
import cloudofficeprint as cop


# Setup Cloud Office Print server
SERVER_URL = "https://api.cloudofficeprint.com/"
API_KEY = "YOUR_API_KEY"  # Replace by your own API key

server = cop.config.Server(
    SERVER_URL,
    cop.config.ServerConfig(api_key=API_KEY)
)


# Let's say we have 100 different customers for who we need to fill in the template and we want to merge the resulting files into a PDF.
# In this example, we are just going to repeat the property 'test' with value 'test' 100 times, but normally you would have different data for each customer.
data = {
    'file'+str(i): cop.elements.Property('test', 'test') for i in range(100)
}


# Create output configuration: merge PDF
conf = cop.config.OutputConfig(
    filetype='pdf',
    pdf_options=cop.config.PDFOptions(
        merge=True
    )
)


# Let's assume that the Cloud Office Print server can't handle all the data at once, so we need to split our data into multiple requests.
# Let's use 10 requests with each 10 elements in the data (a total of 100 data elements).
output_files: List[cop.Response] = []
for i in range(10):
    # Create print job with 10 data elements
    printjob = cop.PrintJob(
        data={
            # Select 10 data elements from the data
            k[0]: k[1] for k in list(data.items())[i*10: (i+1)*10]
        },
        server=server,
        template=cop.Resource.from_local_file(
            './examples/multiple_request_merge_example/template.docx'),
        output_config=conf
    )

    # Execute the print job and save the response to a list
    output_files.append(printjob.execute())


# Create the final request to merge all the received (merged) PDFs
# Create Resource-objects from the Response-objects in output_files
resources = []
for response in output_files:
    resources.append(
        cop.Resource.from_raw(
            raw_data=response.binary,
            filetype='pdf'
        )
    )

# Create the print job for the last request that merges the 10 merged PDF's
# As the template we pick the first PDF in the resources-list
# The other 9 PDFs from the resources-list can be added to append_files (or prepend_files)
printjob = cop.PrintJob(
    data=cop.elements.Property('not_used', 'not_used'),
    server=server,
    template=resources[0],
    append_files=resources[1:]
)
printjob.execute().to_file('./examples/multiple_request_merge_example/output')
