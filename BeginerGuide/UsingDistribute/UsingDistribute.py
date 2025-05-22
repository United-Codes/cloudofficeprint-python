import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop 

# Main data collection 
collection = cop.elements.ElementCollection()

#products
product_a = [
    {"product_name": "Business Shirt", "price": 50, "category": "Mens"},
    {"product_name": "Trousers", "price": 80, "category": "Mens"},
    {"product_name": "Jacket", "price": 150, "category": "Mens"},
    {"product_name": "Blouse", "price": 60, "category": "Womens"}
]
product_b = [
    {"product_name": "Ladies Shoes", "price": 120, "category": "Womens"},
    {"product_name": "Belt", "price": 30, "category": "Accessories"},
    {"product_name": "Bag", "price": 125, "category": "Accessories"},
    {"product_name": "Mens Shoes", "price": 110, "category": "Mens"}
]


product_a_elems = [cop.elements.ElementCollection.from_mapping(p) for p in product_a]
product_b_elems = [cop.elements.ElementCollection.from_mapping(p) for p in product_b]

collection.add(cop.elements.loops.ForEachInline("product_a", product_a_elems))
collection.add(cop.elements.loops.ForEachInline("product_b", product_b_elems, distribute=True))

# orderdata
orders = [
    {
        "order_name": "Order 1",
        "order_total": 2380,
        "product": [
            {"product_name": "Business Shirt", "quantity": 3, "unit_price": 50},
            {"product_name": "Trousers", "quantity": 3, "unit_price": 80},
            {"product_name": "Jacket", "quantity": 3, "unit_price": 150},
            {"product_name": "Blouse", "quantity": 3, "unit_price": 60}
        ]
    },
    {
        "order_name": "Order 2",
        "order_total": 1640,
        "product": [
            {"product_name": "Blouse", "quantity": 4, "unit_price": 60},
            {"product_name": "Skirt", "quantity": 4, "unit_price": 80},
            {"product_name": "Ladies Shoes", "quantity": 4, "unit_price": 120},
            {"product_name": "Bag", "quantity": 4, "unit_price": 125}
        ]
    },
    {
        "order_name": "Order 3",
        "order_total": 730,
        "product": [
            {"product_name": "Blouse", "quantity": 4, "unit_price": 60},
            {"product_name": "Skirt", "quantity": 3, "unit_price": 80},
            {"product_name": "Bag", "quantity": 2, "unit_price": 125}
        ]
    }
]
order_elements = []
for order in orders:
    order_col = cop.elements.ElementCollection()
    order_col.add(cop.elements.Property("order_name", order["order_name"]))
    order_col.add(cop.elements.Property("order_total", order["order_total"]))
    
    order_product_elements = [
        cop.elements.ElementCollection.from_mapping(p) for p in order["product"]
    ]
    
    order_col.add(cop.elements.loops.ForEachInline("product", order_product_elements))
    order_elements.append(order_col)

collection.add(cop.elements.loops.ForEachInline("orders", order_elements))

server = cop.config.Server(
    "http://localhost:8010/",
    config=cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

print_job = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file(
        "./data/template.docx"
    )
)

response = print_job.execute()
response.to_file(
    "./output/output.docx"
)