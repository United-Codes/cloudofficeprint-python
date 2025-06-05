import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop 

# Create main collection
collection = cop.elements.ElementCollection()

# Create elements for the loop
element1 = cop.elements.ElementCollection.from_mapping(
    {
        "a": 1,
        "b": 2,
        "c": 3
    }
)

element2 = cop.elements.ElementCollection.from_mapping(
    {
        "a": 4,
        "b": 5,
        "c": 6
    }
)

# Create  loop
loop = cop.elements.loops.ForEachInline(
    name="loop_name",
    content=[element1, element2]
)

# Add loop to collection
collection.add(loop)

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job with output type specified
# For running on localhost you do not need api_key else replace below "YOUR_API_KEY" with your api key.
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key = "YOUR_API_KEY")
)
# Create print job
# PrintJob combines template, data, server and an optional output configuration
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/loop_template.docx"),
)
# Execute and save
response = printjob.execute()
response.to_file("./output/output_loop.docx")