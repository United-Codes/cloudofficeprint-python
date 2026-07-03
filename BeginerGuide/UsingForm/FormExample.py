import sys
sys.path.insert(0, "PATH TO_COP_DIR")
import cloudofficeprint as cop

# Create an ElementCollection to hold all form elements
collection = cop.elements.ElementCollection()

# Textboxes
collection.add(cop.elements.Textbox(name="first_name"))
collection.add(cop.elements.Textbox(name="last_name", value="Apex R&D", height=20, width=200, multiline=True))

# Radio buttons
collection.add(cop.elements.RadioButton(name="radiolist", value="List A", text="Option A", selected=False))
collection.add(cop.elements.RadioButton(name="radiolist", value="List b", text="List Option b", selected=True))

# Checkbox
collection.add(cop.elements.Checkbox(name="checkbox", value=True, text="Agree to terms"))

# Dropdown and ComboBox
collection.add(cop.elements.Dropdown(
    "country",
    [{"value": "US", "label": "United States"}, {"value": "BE", "label": "Belgium"}, {"value": "NP", "label": "Nepal"}],
    "BE", 20, 200,
))
collection.add(cop.elements.ComboBox(
    "city",
    [{"value": "Ghent"}, {"value": "Kathmandu"}],
    "Pokhara", 20, 200,
))

# ListBox
collection.add(cop.elements.ListBox(
    "roles",
    [{"value": "admin", "label": "Admin"}, {"value": "user", "label": "User"}, {"value": "guest", "label": "Guest"}],
    ["admin", "user"], True, 80, 200,
))

# Push button and password field
collection.add(cop.elements.PushButton("submit", "Submit form", 24, 120))
collection.add(cop.elements.Password("pw", "s3cret", 20, 200))

#  Configure the Server 
server = cop.config.Server(
    url="http://localhost:8010/",
    config=cop.config.ServerConfig(api_key="YOUR_API_KEY"),
)

#  Load the DOCX Template 
template = cop.Resource.from_local_file("./data/template.docx")
output_conf = cop.config.OutputConfig(filetype="pdf")

#  Create and Run the PrintJob 
printjob = cop.PrintJob(
    data=collection,
    template=template,
    server=server,
    output_config=output_conf,
)
response = printjob.execute()
response.to_file("./output/output.pdf")
