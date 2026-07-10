import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop

collection = cop.elements.ElementCollection("collection")

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Sign the output PDF with a certificate & password
pdf_options = cop.config.PDFOptions()
pdf_options.sign(
    cop.Resource.from_local_file("./data/certificate.p12"),
    "cloudofficeprint",
)
pdf_options.sign_certificate_txt = "Signed by Cloud Office Print"

output_config = cop.config.OutputConfig(filetype="pdf", pdf_options=pdf_options)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.pdf"),
    output_config=output_config
)

# Execute and save 
response = printjob.execute()
response.to_file("./output/output.pdf")
