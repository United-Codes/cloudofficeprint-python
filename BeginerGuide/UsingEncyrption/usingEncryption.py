import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop

# Main object that holds the data
collection = cop.elements.ElementCollection()

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
text2 = cop.elements.Property(
    name="text2",
    value="This is an example created with the Cloud Office Print Python SDK"
)
collection.add(text2)
# Server 
server = cop.config.Server(
    url="http://localhost:8010/",
    config=cop.config.ServerConfig(api_key="YOUR_API_KEY")  
)

# Template 
template = cop.Resource.from_local_file("./data/template.docx")

output_conf = cop.config.OutputConfig(filetype="pdf",
    output_read_password="123"
)

# PrintJob 
printjob = cop.PrintJob(
    data=collection,
    template=template,
    server=server,
    output_config=output_conf,
)
response = printjob.execute()
response.to_file("./output/output.pdf")
