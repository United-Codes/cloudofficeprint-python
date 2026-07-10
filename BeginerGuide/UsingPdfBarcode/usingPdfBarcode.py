import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop

collection = cop.elements.ElementCollection()

collection.add(cop.elements.BarCode("product_barcode", "1234567890", "code128", 50, 100))

collection.add(cop.elements.QRCode("product_qr", "https://www.cloudofficeprint.com/", "qrcode"))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

pdf_options = cop.config.PDFOptions(insert_barcode=True)
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
