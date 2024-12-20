# Install cloudofficeprint using  pip install cloudofficeprint
#Import the cloudofficeprint libary.
import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop

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

docx_column1_cell_style = cop.elements.CellStyleDocx(
        cell_background_color='red',
        border_color='0d72c7',
        border_top='double',
        border_top_size=20,
        border_left='dotDash',
        border_bottom_color='yellow',
        border_left_size='38'
    )
docx_column1_table_style_property = cop.elements.CellStyleProperty(
        name='column1',
        value='DemoCustomerName',
        cell_style=docx_column1_cell_style
    )
collection.add(docx_column1_table_style_property)

docx_column2_cell_style = cop.elements.CellStyleDocx(
        border_right_space=15,
        border_diagonal_down='single',
        border_diagonal_down_size=10,
        border_diagonal_up='single',
        border_diagonal_up_color='#0d72c7'
    )
docx_column2_table_style_property = cop.elements.CellStyleProperty(
        name='column2',
        value='DemoCustomerName',
        cell_style=docx_column2_cell_style
    )
collection.add(docx_column2_table_style_property)

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
    template=cop.Resource.from_local_file("D:/UC/cloudofficeprint-python/BeginerGuide/UsingElements/data/template.docx"),
)
# Execute print job and save response to file
response = printjob.execute()
response.to_file("D:/UC/cloudofficeprint-python/BeginerGuide/UsingElements/output/output.docx")