import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop



# Main object that holds the data
collection = cop.elements.ElementCollection()
collection.add(cop.elements.Property("title", "Hello World!"))
collection.add(cop.elements.Property("text", "This document is used to extract metadata."))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

output_config = cop.config.OutputConfig(filetype="meta_data")

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.docx"),
    output_config=output_config
)

# Execute and print/save the returned metadata
response = printjob.execute()
print(response.to_string())
response.to_file("./output/metadata.json")
