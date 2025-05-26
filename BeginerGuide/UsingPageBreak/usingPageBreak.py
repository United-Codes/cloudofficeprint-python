import sys
sys.path.insert(0, "Path_To_Dir")
import cloudofficeprint as cop 


# Create main data collection
collection = cop.elements.ElementCollection()

# Add customer data
customer1 = cop.elements.ElementCollection()
customer1.add(cop.elements.Property("cust_first_name", "John"))
customer1.add(cop.elements.Property("cust_last_name", "Dulles"))
customer1.add(cop.elements.PageBreak("pageBreak", True))

customer2 = cop.elements.ElementCollection()
customer2.add(cop.elements.Property("cust_first_name", "William"))
customer2.add(cop.elements.Property("cust_last_name", "Hartsfield"))
customer2.add(cop.elements.PageBreak("pageBreak", True))

customer3 = cop.elements.ElementCollection()
customer3.add(cop.elements.Property("cust_first_name", "Edward"))
customer3.add(cop.elements.Property("cust_last_name", "Logan"))
customer3.add(cop.elements.PageBreak("pageBreak", False))

# Create customers loop
customers_loop = cop.elements.ForEach("customers", [customer1, customer2, customer3])
collection.add(customers_loop)

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/", 
    cop.config.ServerConfig(api_key="YOUR_API_KEY")  
)

# Load template and create print job
template = cop.Resource.from_local_file("./data/pagebreak_temp.docx")
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=template
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output.docx")