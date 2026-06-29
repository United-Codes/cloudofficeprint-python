import sys
# sys.path.insert(0, "PATH_TO_COP_DIR")
sys.path.insert(0, "C:/Users/em8ee/cloudofficeprint-python")
import cloudofficeprint as cop

customers = [
    {"sheet_name": "John Dulles", "cust_first_name": "John", "cust_last_name": "Dulles", "cust_city": "Sterling", "orders": [{"order_name": "Order 1", "order_total": 2380}]},
    {"sheet_name": "William Hartsfield", "cust_first_name": "William", "cust_last_name": "Hartsfield", "cust_city": "Atlanta", "orders": [{"order_name": "Order 1", "order_total": 1640}, {"order_name": "Order 2", "order_total": 730}]},
    {"sheet_name": "Edward Logan", "cust_first_name": "Edward", "cust_last_name": "Logan", "cust_city": "East Boston", "orders": [{"order_name": "Order 1", "order_total": 1515}, {"order_name": "Order 2", "order_total": 905}]},
    {"sheet_name": "Frank OHare", "cust_first_name": "Frank", "cust_last_name": "OHare", "cust_city": "Chicago", "orders": [{"order_name": "Order 1", "order_total": 1060}]},
    {"sheet_name": "Eugene Bradley", "cust_first_name": "Eugene", "cust_last_name": "Bradley", "cust_city": "Windsor Locks", "orders": [{"order_name": "Order 1", "order_total": 1890}, {"order_name": "Order 2", "order_total": 870}]},
]

# Create main collection
collection = cop.elements.ElementCollection()

# Create sheet loop
loop = cop.elements.loops.ForEachSheet(
    name="customers",
    content=[cop.elements.ElementCollection.from_mapping(customer) for customer in customers]
)
collection.add(loop)

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

output_config = cop.config.OutputConfig(
    filetype="xlsx",
    output_export_sheets=["John Dulles", "Edward Logan"]
)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.xlsx"),
    output_config=output_config
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output.xlsx")
