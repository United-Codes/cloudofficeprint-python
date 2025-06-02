import sys
sys.path.insert(0, "PATH_TO_COP_DIR")  
import cloudofficeprint as cop

# Main object that holds the data
data = cop.elements.ElementCollection()

# Define  customers data 
customers_data = [
    {
        "sheet_name": "John Dulles",
        "cust_first_name": "John",
        "cust_last_name": "Dulles",
        "cust_city": "Sterling",
        "orders": [
            {"order_total": 2380, "order_name": "Order 1"}
        ]
    },
    {
        "sheet_name": "William Hartsfield",
        "cust_first_name": "William",
        "cust_last_name": "Hartsfield",
        "cust_city": "Atlanta",
        "orders": [
            {"order_total": 1640, "order_name": "Order 1"},
            {"order_total":  730, "order_name": "Order 2"}
        ]
    },
    {
        "sheet_name": "Edward Logan",
        "cust_first_name": "Edward",
        "cust_last_name": "Logan",
        "cust_city": "East Boston",
        "orders": [
            {"order_total": 1515, "order_name": "Order 1"},
            {"order_total":  905, "order_name": "Order 2"}
        ]
    },
    {
        "sheet_name": "Frank OHare",
        "cust_first_name": "Frank",
        "cust_last_name": "OHare",
        "cust_city": "Chicago",
        "orders": []          #Note: set this to [] or none to trigger the hide

    },
    {
        "sheet_name": "Cris Jr Santos",
        "cust_first_name": "Cris Jr",
        "cust_last_name": "Santos",
        "cust_city": "Texas",
        "orders": []          #Note: set this to [] or none to trigger the hide
    }
]

#Build up a Py list of ElementCollection objects for each customer
customers_list = []
for customer in customers_data:
    mapping = {
        "sheet_name":      customer["sheet_name"],
        "cust_first_name": customer["cust_first_name"],
        "cust_last_name":  customer["cust_last_name"],
        "cust_city":       customer["cust_city"],

    }
    customer_elem = cop.elements.ElementCollection.from_mapping(mapping)

    if customer.get("orders"):
        order_elems = [
            cop.elements.ElementCollection.from_mapping({
                "order_total": o["order_total"],
                "order_name":  o["order_name"]
            })
            for o in customer["orders"]
        ]
        customer_elem.add(cop.elements.ForEach("orders", order_elems))
    else:
        # If orders is empty or None, explicitly set "orders" to None so that
        # !orders == true in the template:
        customer_elem.add(
            cop.elements.ElementCollection.from_mapping({"orders": None})
        )
    customers_list.append(customer_elem)

# wrap all customers 
customers_cursor = cop.elements.ForEach("customers", customers_list)
data.add(customers_cursor)

server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)
printjob = cop.PrintJob(
    data=data,
    server=server,
    template=cop.Resource.from_local_file("./data/hide_temp.pptx")
)


response = printjob.execute()
response.to_file("./output/output")
