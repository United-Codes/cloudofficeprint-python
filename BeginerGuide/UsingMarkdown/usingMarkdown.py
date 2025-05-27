import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop 


# Create main data collection
collection = cop.elements.ElementCollection()

#markdown content
markdown_text = """
# Heading level 1

## Heading level 2

===============

I just love **bold text**.  

Italicized text is the *cat's meow*.

1. First item
2. Second item
3. Third item
4. Fourth item

---

* First item
* Second item
* Third item
* Fourth item

| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |

<strike>The world is flat.</strike> We now know that the world is round.
"""
# Adding markdown content 
collection.add(cop.elements.MarkdownContent("markdowncontent", markdown_text))

# Create and add customer names
cust_names = cop.elements.ElementCollection("cust_names")
customers = [
    {"first": "Albert", 
     "cust_name_bold": "**Albert**"},
    {"first": "Edward", 
     "cust_name_bold": "**Edward**"},
    {"first": "Eugene", 
     "cust_name_bold": "**Eugene**"},
    {"first": "Fiorello",
      "cust_name_bold": "**Fiorello**"},
    {"first": "Frank", 
     "cust_name_bold": "**Frank**"},
    {"first": "John",
      "cust_name_bold": "**John**"},
    {"first": "William",
      "cust_name_bold": "**William**"}
]

customer_collections = []
for customer in customers:
    cust_collection = cop.elements.ElementCollection()
    cust_collection.add(cop.elements.Property("first", customer["first"]))
    cust_collection.add(cop.elements.Property("cust_name_bold", customer["cust_name_bold"]))
    customer_collections.append(cust_collection)

# create array structure
customers_loop = cop.elements.ForEach("cust_names", customer_collections)
collection.add(customers_loop)


# Server configuration
server = cop.config.Server(
    "http://localhost:8010/", 
    cop.config.ServerConfig(api_key="YOUR_API_KEY")  
)

# Load template and create print job
template = cop.Resource.from_local_file("./data/template.docx")
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=template
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output")