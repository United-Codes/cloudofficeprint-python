import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop

invoices = [
    {"invoice_no": "INV-001", "amount": "$100"},
    {"invoice_no": "INV-002", "amount": "$200"},
    {"invoice_no": "INV-003", "amount": "$300"},
]

# Main object that holds the data
collection = cop.elements.ElementCollection()
collection.add(cop.elements.ForEach(
    "invoices",
    [cop.elements.ElementCollection.from_mapping(inv) for inv in invoices],
))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

pdf_options = cop.config.PDFOptions(split=True, split_by_string="Invoice No")
output_config = cop.config.OutputConfig(filetype="pdf", pdf_options=pdf_options)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.docx"),
    output_config=output_config
)

# Execute and save the response 
response = printjob.execute()
response.to_file("./output/output.zip")
