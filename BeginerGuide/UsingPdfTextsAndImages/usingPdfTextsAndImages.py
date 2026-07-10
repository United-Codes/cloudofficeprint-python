import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop

collection = cop.elements.ElementCollection("collection")

collection.add(cop.elements.PDFTexts([
    cop.elements.PDFText(
        text="Hello from Cloud Office Print",
        x=50,
        y=50,
        page="all",
        rotation=0,
        bold=True,
        italic=False,
        font_color="#FF0000",
        font_size=20,
    ),
]))

image = cop.own_utils.file_utils.read_file_as_base64("./data/image.png")
collection.add(cop.elements.PDFImages([
    cop.elements.PDFImage(
        image=image,
        x=50,
        y=100,
        page=1,
        rotation=0,
        width=120,
        height=120,
    ),
]))

# Server configuration
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)

# Create print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.pdf"),
    output_config=cop.config.OutputConfig(filetype="pdf")
)

# Execute and save
response = printjob.execute()
response.to_file("./output/output.pdf")
