import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import cloudofficeprint as cop

collection = cop.elements.ElementCollection()

collection.add(cop.elements.Property("customer_name", "John Doe"))
collection.add(cop.elements.Property("invoice_number", "INV-2025-001"))
collection.add(cop.elements.Property("issue_date", "2024-06-15"))
collection.add(cop.elements.Property("amount", "$1,500.00"))

collection.add(cop.elements.Property(
    "company_logo",
    cop.own_utils.file_utils.read_file_as_base64("./data/image.png"),
))


def employee(name: str, role: str) -> cop.elements.ElementCollection:
    e = cop.elements.ElementCollection()
    e.add(cop.elements.Property("name", name))
    e.add(cop.elements.Property("role", role))
    return e


collection.add(cop.elements.ForEach("employees", [
    employee("Alice", "Engineer"),
    employee("Bob", "Manager"),
    employee("Carol", "Designer"),
]))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job with the PDF template
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.pdf"),
    output_config=cop.config.OutputConfig(filetype="pdf")
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output.pdf")
