import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop 

# Create main collection
collection = cop.elements.ElementCollection()

# Create elements for the labels
element1 = cop.elements.ElementCollection.from_mapping(
    {
        "FirstName": "John",
        "LastName": "Smith",
        "Company": "Tech Solutions Inc.",
        "Address1": "123 Business Ave",
        "City": "San Francisco",
        "State": "CA",
        "PostalCode": "94105"
    }
)
element2 = cop.elements.ElementCollection.from_mapping(
    {
        "FirstName": "Sarah",
        "LastName": "Johnson",
        "Company": "Marketing Pro LLC",
        "Address1": "456 Market Street",
        "City": "New York",
        "State": "NY",
        "PostalCode": "10013"
    }
)
element3 = cop.elements.ElementCollection.from_mapping(
    {
        "FirstName": "Michael",
        "LastName": "Brown",
        "Company": "Digital Services Co.",
        "Address1": "789 Innovation Blvd",
        "City": "Chicago",
        "State": "IL",
        "PostalCode": "60601"
    }
)

loopLabel = cop.elements.loops.Labels(
    name="labels",
    content=[element1, element2, element3]
)
#  Add the loop to the main collection
collection.add(loopLabel)

# Server 
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/label_temp.docx")
)

# Execute and save the output
response = printjob.execute()
response.to_file("./output/label_output.docx")