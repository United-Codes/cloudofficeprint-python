import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop 


# Create data collection
collection = cop.elements.ElementCollection()

# HTML paragraph and line break
collection.add(cop.elements.Html(
    name="overview",
    value=(
        "<p>This is a <strong>bold</strong> statement, followed by a line break.<br />"
        "And here's a new line in the same paragraph.</p>"
    ),
    custom_table_style   = None,
    unordered_list_style = None,
    ordered_list_style   = None,
    use_tag_style        = None,
    ignore_cell_margin   = None,
    ignore_empty_p       = None
))

# empty paragraphs
collection.add(cop.elements.Html(
    name="html_with_empty_p",
    value="<p>First paragraph.</p> <p></p> <p>Third paragraph.</p>",
    custom_table_style   = None,
    unordered_list_style = None,
    ordered_list_style   = None,
    use_tag_style        = None,
    ignore_cell_margin   = None,
    ignore_empty_p       = True
))

# Word’s tag style and also set a custom numbering style
collection.add(cop.elements.Html(
    name="lists",
    value=(
        "<ul>"
        "  <li>Level 1"
        "    <ol>"
        "      <li>Sub-item A</li>"
        "      <li>Sub-item B</li>"
        "    </ol>"
        "  </li>"
        "  <li>Level 2</li>"
        "</ul>"
    ),
    custom_table_style=None,
    unordered_list_style="1",    
    ordered_list_style="2",  
    use_tag_style=True,
    ignore_cell_margin=None,
    ignore_empty_p=True          
))

#HTML table (default style)
collection.add(cop.elements.Html(
    name="html_table_1",
    value=(
        '<table border="1">'
        '  <tr><th>Name</th><th>Age</th><th>Country</th></tr>'
        '  <tr><td>Alice</td><td>30</td><td>USA</td></tr>'
        '  <tr><td>Bob</td><td>25</td><td>Canada</td></tr>'
        '</table>'
    ),
    custom_table_style   = None,
    unordered_list_style = None,
    ordered_list_style   = None,
    use_tag_style        = None,
    ignore_cell_margin   = None,
    ignore_empty_p       = None
))

# <img> tag
collection.add(cop.elements.Html(
    name="html_img",
    value=(
        '<img src="https://picsum.photos/200/100" '
        'width="100px" height="50px" />'
    ),
    custom_table_style   = None,
    unordered_list_style = None,
    ordered_list_style   = None,
    use_tag_style        = None,
    ignore_cell_margin   = None,
    ignore_empty_p       = None
))

# server
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)
template = cop.Resource.from_local_file("./data/html_temp.docx")

# print job
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=template
)

# save output 
response = printjob.execute()
response.to_file("./output/output")
