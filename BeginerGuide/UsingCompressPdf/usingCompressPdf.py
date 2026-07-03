import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop

# Main object that holds the data
collection = cop.elements.ElementCollection()
collection.add(cop.elements.Property("title", "Hello World!"))
collection.add(cop.elements.Property("text", "This PDF is compressed to reduce its file size."))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

pdf_options = cop.config.PDFOptions(compress_pdf=True)
output_config = cop.config.OutputConfig(filetype="pdf", pdf_options=pdf_options)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.docx"),
    output_config=output_config
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output.pdf")
