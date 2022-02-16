# Install cloudofficeprint using  pip install cloudofficeprint
import cloudofficeprint as cop #Import the cloudofficeprint libary.
# Main object that holds the data
collection = cop.elements.ElementCollection()
# Create the title element and add it to the element collection
title = cop.elements.Property(
    name="title",
    value="Hello World!"
)
collection.add(title)

# Create the text element and add it to the element collection
text = cop.elements.Property(
    name="text",
    value="This is an example created with the Cloud Office Print Python SDK"
)
collection.add(text)

# configure server
# For running on localhost you do not need api_key else replace below "YOUR_API_KEY" with your api key.
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key = "YOUR_API_KEY")
)
# Create print job
# PrintJob combines template, data, server and an optional output configuration
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.docx"),
)
# Execute print job and save response to file
response = printjob.execute()
response.to_file("output/output")