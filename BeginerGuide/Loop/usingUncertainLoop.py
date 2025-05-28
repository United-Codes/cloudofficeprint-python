import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop

# Create main collection
collection = cop.elements.ElementCollection()

# Create products data
products = [
    {"prod_name": "Business Shirt", "category": "Mens"},
    {"prod_name": "Trousers", "category": "Mens"},
    {"prod_name": "Jacket", "category": "Mens"},
    {"prod_name": "Blouse", "category": "Womens"},
    {"prod_name": "Skirt", "category": "Womens"},
    {"prod_name": "Ladies Shoes", "category": "Womens"},
    {"prod_name": "Belt", "category": "Accessories"},
    {"prod_name": "Bag", "category": "Accessories"},
    {"prod_name": "Mens Shoes", "category": "Mens"},
    {"prod_name": "Wallet", "category": "Accessories"}
]

#elements for each product item
product_elements = []
for product in products:
    element_collection = cop.elements.ElementCollection()
    element_collection.add(cop.elements.Property("prod_name", product["prod_name"]))
    element_collection.add(cop.elements.Property("category", product["category"]))
    product_elements.append(element_collection)

#ForEach loop
collection.add(cop.elements.ForEach(name="products", content=product_elements))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job
template = cop.Resource.from_local_file("./data/un_loop.docx")
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=template
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output1.docx")