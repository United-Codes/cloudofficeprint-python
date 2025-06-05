import sys
sys.path.insert(0, "Path_To_Dir")
import cloudofficeprint as cop 

# Create main data collection
collection = cop.elements.ElementCollection()

collection.add(cop.elements.Property("cust_first_name", "John"))
collection.add(cop.elements.Property("cust_last_name", "Doe"))

# Create a span element for the first cell that will span 2 rows and 3 columns
span1 = cop.elements.Span(
    name="span",
    value="This cell will span 2 rows and 3 columns",
    columns=3,
    rows=2
)

# Create a span element for the second cell that will span 3 rows and 4 columns 
span2 = cop.elements.Span(
    name="testSpan",
    value="This cell will span 3 rows and 4 columns",
    columns=4,
    rows=3
)

# Add spans to collection
collection.add(span1)
collection.add(span2)

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/", 
    cop.config.ServerConfig(api_key="YOUR_API_KEY")  
)

# Load template and create print job
template = cop.Resource.from_local_file("./data/span_temp.xlsx")
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=template
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output")