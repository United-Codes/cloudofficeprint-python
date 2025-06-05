import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop 

# Create main collection
collection = cop.elements.ElementCollection()

# Create elements for customer invoices
element1 = cop.elements.ElementCollection.from_mapping(
    {
        "cust_first_name": "John",
        "cust_last_name": "Smith",
        "orders": [
            {"order_name": "Office Supplies", "order_total": "$525.00"},
            {"order_name": "Electronics", "order_total": "$1,299.99"},
            {"order_name": "Furniture", "order_total": "$2,450.00"}
        ]
    }
)

element2 = cop.elements.ElementCollection.from_mapping(
    {
        "cust_first_name": "Sarah",
        "cust_last_name": "Johnson",
        "orders": [
            {"order_name": "Software License", "order_total": "$899.00"},
            {"order_name": "IT Support", "order_total": "$750.00"}
        ]
    }
)

element3 = cop.elements.ElementCollection.from_mapping(
    {
        "cust_first_name": "Michael",
        "cust_last_name": "Brown",
        "orders": [
            {"order_name": "Marketing Services", "order_total": "$3,500.00"},
            {"order_name": "Training Materials", "order_total": "$450.00"},
            {"order_name": "Cloud Storage", "order_total": "$199.99"}
        ]
    }
)

# Create sheet loop
loop = cop.elements.loops.ForEachSheet(
    name="customers",
    content=[element1, element2, element3]
)

# Add loop to collection
collection.add(loop)

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/shhet_temp.xlsx")
)

# Execute and save
response = printjob.execute()
response.to_file("./output/sheet_output.xlsx")