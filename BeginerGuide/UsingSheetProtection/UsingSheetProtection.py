# Install cloudofficeprint using  pip install cloudofficeprint
import cloudofficeprint as cop 

# Main object that holds the data
collection = cop.elements.ElementCollection()

# Use SheetProtection to protect the sheet with a password
sheet_protection = cop.elements.SheetProtection(
    name="protectTag",
    password="123",  
    formatCells=False,
    insertRows=False,
    deleteRows=False
)
collection.add(sheet_protection)

fname = cop.elements.Property(name="cust_first_name", value="john")
collection.add(fname)

lname = cop.elements.Property(name="cust_last_name", value="doe")
collection.add(lname)

# configure server
# For running on localhost you do not need api_key else replace below "YOUR_API_KEY" with your api key.
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key = "YOUR_API_KEY")
)
# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/temp.xlsx"),
)
# Execute print job and save response to file
response = printjob.execute()
response.to_file("./output/output.xlsx")