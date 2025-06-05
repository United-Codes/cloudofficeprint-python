import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop 

# Create main data collection
collection = cop.elements.ElementCollection()
greeting = cop.elements.PptxShapeRemove("greeting", "Hello World, Thank you for using AOP")
collection.add(greeting)

# The remove property will be false, so any shape with {remove?} tag will be removed in the tenmlate
remove = cop.elements.PptxShapeRemove("remove", False)
collection.add(remove)

# Add a quote that will be shown
quote = cop.elements.PptxShapeRemove("toShow", "When in doubt, look intelligent. - GARRISON KEILLOR")
collection.add(quote)

# Configure server 
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/shapeRemove_temp.pptx")
)

# Execute print job and save response to file
response = printjob.execute()
response.to_file("./output/output.pptx")