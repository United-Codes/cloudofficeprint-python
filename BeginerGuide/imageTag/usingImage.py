import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop 

# Create data collection
collection = cop.elements.ElementCollection()

# Add sample properties
collection.add(cop.elements.Property(name="title",       value="Image Example"))
collection.add(cop.elements.Property(name="description", value="This images are dynamically loaded using Cloud Office Print"))

# 1) URL based image
image = cop.elements.Image.from_url(
    name="image_name",  
    url_source="https://picsum.photos/300/200",
    width="80px",
    height="60px",
    alt_text="Random image",
    wrap_text="square",
    rotation=0,
    transparency="10%",
    url="https://example.com"
)
collection.add(image)

# 2) SVG with density 
image_svg = cop.elements.Image.from_url(
    name="img_svg",
    url_source="https://upload.wikimedia.org/wikipedia/commons/4/4f/SVG_Logo.svg",
    width="200px",
    density=300,      # 300 dpi
    alt_text="SVG logo",
)
collection.add(image_svg)

# 3) Local file image
collection.add(
    cop.elements.Image.from_file(
        name="img_file",
        path="./local_img/UC_Logo.svg",
        width="150px",    
        wrap_text="square",
        alt_text=" Uc logo"
    )
)

#server
server = cop.config.Server(
    "http://localhost:8010/", 
    cop.config.ServerConfig(api_key="YOUR_API_KEY")  
)

# Load template
template = cop.Resource.from_local_file("./data/img_temp.docx")

# print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=template
)

#save output 
response = printjob.execute()
response.to_file("./output/ouput")
