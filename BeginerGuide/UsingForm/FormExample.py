import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop

# Create an ElementCollection to hold all form elements
collection = cop.elements.ElementCollection()

# Textboxes
first_name_collection = cop.elements.ElementCollection("first_name")
first_name_collection.add(
    cop.elements.Textbox(name="first_name", value="Prabin")
)
last_name_collection = cop.elements.ElementCollection("last_name")
last_name_collection.add(
    cop.elements.Textbox(
        name="last_name",
        value="Apex R&D",
        width=200,
        height=20,
        multiline=True
    )
)
collection.add(first_name_collection)
collection.add(last_name_collection)

# Radio buttons
radiolist_collection = cop.elements.ElementCollection("radiolist")
radiolist_collection.add(
    cop.elements.RadioButton(
        name="radiolist",
        value="List A",
        text="List Option A",
        selected=True
    )
)
radiolist_collection.add(
    cop.elements.RadioButton(
        name="radiolist",
        value="List B",
        text="List Option B"
    )
)
collection.add(radiolist_collection)

# checkbox 
checkbox_collection = cop.elements.ElementCollection("checkbox")
checkbox_collection.add(
    cop.elements.Checkbox(
        name="checkbox",
        value=True,
        text="IsChecked",
        height=20,
        width=200
    )
)
collection.add(checkbox_collection)

#  Configure the Server 
server = cop.config.Server(
    url="http://localhost:8010/",
    config=cop.config.ServerConfig(api_key="YOUR_API_KEY")  
)

#  Load the DOCX Template 
template = cop.Resource.from_local_file("C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python/BeginerGuide/UsingForm/data/template.docx")
output_conf = cop.config.OutputConfig(filetype="pdf")

#  Create and Run the PrintJob 
printjob = cop.PrintJob(
    data=collection,
    template=template,
    server=server,
    output_config=output_conf,
)
response = printjob.execute()
response.to_file( "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python/BeginerGuide/UsingForm/output/output.pdf")


