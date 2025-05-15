import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop 

root = cop.elements.ElementCollection()

file_entry = cop.elements.ElementCollection.from_mapping({
    "filename": "department_report.docx"
})

data_content = cop.elements.ElementCollection("data")


product_a = [
    {"product_name": "Business Shirt", "price": 50,  "category": "Mens"},
    {"product_name": "Trousers",       "price": 80,  "category": "Mens"},
    {"product_name": "Jacket",         "price": 150, "category": "Mens"},
    {"product_name": "Blouse",         "price": 60,  "category": "Womens"},
]
product_b = [
    {"product_name": "Ladies Shoes", "price": 120, "category": "Womens"},
    {"product_name": "Belt",         "price": 30,  "category": "Accessories"},
    {"product_name": "Bag",          "price": 125, "category": "Accessories"},
    {"product_name": "Mens Shoes",   "price": 110, "category": "Mens"},
]


product_a_elems = [cop.elements.ElementCollection.from_mapping(p) for p in product_a]
product_b_elems = [cop.elements.ElementCollection.from_mapping(p) for p in product_b]

data_content.add(
    cop.elements.loops.ForEachInline("product_a", product_a_elems, distribute=False)
)
data_content.add(
    cop.elements.loops.ForEachInline("product_b", product_b_elems, distribute=True)
)
orders_data = [
    {
        "order_name":  "Order 1",
        "order_total": 2380,
        "product": [
            {"product_name": "Business Shirt", "quantity": 3, "unit_price": 50},
            {"product_name": "Trousers",       "quantity": 3, "unit_price": 80},
            {"product_name": "Jacket",         "quantity": 3, "unit_price": 150},
            {"product_name": "Blouse",         "quantity": 3, "unit_price": 60},
        ],
    },
    {
        "order_name":  "Order 2",
        "order_total": 1640,
        "product": [
            {"product_name": "Blouse",       "quantity": 4, "unit_price": 60},
            {"product_name": "Skirt",        "quantity": 4, "unit_price": 80},
            {"product_name": "Ladies Shoes", "quantity": 4, "unit_price": 120},
            {"product_name": "Bag",          "quantity": 4, "unit_price": 125},
        ],
    },
    {
        "order_name":  "Order 3",
        "order_total": 730,
        "product": [
            {"product_name": "Blouse", "quantity": 4, "unit_price": 60},
            {"product_name": "Skirt",  "quantity": 3, "unit_price": 80},
            {"product_name": "Bag",    "quantity": 2, "unit_price": 125},
        ],
    },
]

order_collections = []
for o in orders_data:
    oc = cop.elements.ElementCollection()
    oc.add(cop.elements.Property("order_name", o["order_name"]))
    oc.add(cop.elements.Property("order_total", o["order_total"]))
    prod_elems = [
        cop.elements.ElementCollection.from_mapping(p) for p in o["product"]
    ]
    oc.add(cop.elements.loops.ForEachInline("product", prod_elems, distribute=False))
    order_collections.append(oc)

# Wrap all ordersnloop
data_content.add(
    cop.elements.loops.ForEachInline("orders", order_collections, distribute=False)
)


file_entry.add(data_content)
root.add(file_entry)

# print job 
server = cop.config.Server("http://localhost:8010/")
print_job = cop.PrintJob(
    data=root,
    server=server,
    template=cop.Resource.from_local_file(
        "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python/BeginerGuide/UsingDistribute/data/horizontal_tabular_looping_output-ed506eb2e341afbf52e1a05319e2b086.docx"),
)

response = print_job.execute()
response.to_file(
    "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python/BeginerGuide/UsingDistribute/output/output.docx"
)
