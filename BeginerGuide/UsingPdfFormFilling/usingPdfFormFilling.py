import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop




collection = cop.elements.ElementCollection()
collection.add(cop.elements.PDFFormData({
    "name": "Nishant Thapa",
    "email": "nishan@nomail.com",
    "country": "Nepal",
    "subscribe": True,
}))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)


# Create print job 
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.pdf"),
    output_config=cop.config.OutputConfig(filetype="pdf")
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output.pdf")
