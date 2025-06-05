import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop 

# Create main collection
collection = cop.elements.ElementCollection()

# Create elements for the loop
element1 = cop.elements.ElementCollection.from_mapping(
    {
        "a": "Sales Report Q1",
        "b": "Total Revenue: $125,000",
        "c": "Growth: 15% YoY"
    }
)
element2 = cop.elements.ElementCollection.from_mapping(
    {
        "a": "Marketing Metrics Q1",
        "b": "New Customers: 2,500",
        "c": "Campaign ROI: 225%"
    }
)
element3 = cop.elements.ElementCollection.from_mapping(
    {
        "a": "Product Performance Q1",
        "b": "Units Sold: 45,000",
        "c": "Customer Satisfaction: 4.8/5"
    }
)
element4 = cop.elements.ElementCollection.from_mapping(
    {
        "a": "Support Analytics Q1",
        "b": "Tickets Resolved: 3,200",
        "c": "Average Response Time: 2.5h"
    }
)

#slide loop
loop = cop.elements.loops.ForEachSlide(
    name="slideloop",
    content=[element1, element2, element3, element4]
)
#  Add the loop to the main collection
collection.add(loop)

# Server 
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./Loop/data/slide_temp.pptx")
)

# Execute and save the output
response = printjob.execute()
response.to_file("./Loop/output/output")