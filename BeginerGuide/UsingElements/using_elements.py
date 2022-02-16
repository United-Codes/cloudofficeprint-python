# Install cloudofficeprint using  pip install cloudofficeprint
#Import the cloudofficeprint libary.
from ... import cloudofficeprint as cop
# Main object that holds the data
collection = cop.elements.ElementCollection()
# Create the title element and add it to the element collection

# -----------Property--------
prop = cop.elements.Property(
        name='title',
        value='hello World'
    )
collection.add(prop)

# ---------------------using autoLink-----------
autoLink = cop.elements.AutoLink(
        name='autoLink',
        value='sample text with hyperlinks like https://www.cloudofficeprint.com/docs/python/index.html . COP link is https://www.cloudofficeprint.com/index.html contact us in info@cloudofficeprint.com ',
    )
collection.add(autoLink)

# ----------------HyperLink---------------
hyperlink = cop.elements.Hyperlink(
        name='hyperlink',
        url='https://www.cloudofficeprint.com/index.html',
        text='COP_link'
    )
collection.add(hyperlink)

# -------------------styled Property-------
styled_prop = cop.elements.StyledProperty(
        name='styledPropertyName',
        value='DemoCustomerName',
        font='NanumMyeongjo',
        font_size='25pt',
        font_color='#ff00ff',
        bold=True,
        italic=True,
        underline=False,
        strikethrough=False,
        highlight_color='darkMagenta'
    )
collection.add(styled_prop)

# ------------------watermark----------
watermark = cop.elements.Watermark(
        name='watermark_name',
        text='COP Trial',
        color='red',
        font='Arial',
        width=200,
        height=30,
        opacity=50,
        rotation=45
    )
collection.add(watermark)

# configure server
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
    template=cop.Resource.from_local_file("./data/template.docx"),
)
# Execute print job and save response to file
response = printjob.execute()
response.to_file("output/output")