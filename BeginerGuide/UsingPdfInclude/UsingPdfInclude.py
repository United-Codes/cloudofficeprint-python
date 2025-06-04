#Import the cloudofficeprint libary.
import base64
import sys
sys.path.insert(0, "./cloudofficeprint-python")
import cloudofficeprint as cop

# Read the image file and encode it to base64
# Make sure to change the path to the image file as per your system
with open("./data/view.png", "rb") as img:
    # Encode the image to base64
    b64_img = base64.b64encode(img.read()).decode("utf-8")


# Create element collection
collection = cop.elements.ElementCollection()

# include element 
include1 = cop.elements.PdfInclude(
    name="view",
    value="",
    filename="view.pdf",
    mime_type="image/png",
    file_content=b64_img,
    file_source="base64"
    )
collection.add(include1)

#  Configure the Server 
server = cop.config.Server(
    url="http://localhost:8010/",
    config=cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

#  Load the DOCX Template 
template = cop.Resource.from_local_file("./data/include_temp.docx")

#  Create and Run the PrintJob 
printjob = cop.PrintJob(
    data=collection,
    template=template,
    server=server,
    output_config=cop.config.OutputConfig(filetype="pdf")
)
response = printjob.execute()
response.to_file("./output/output")

