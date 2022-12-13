"""This is a standard example of how to use an API to get data to fill in a template.
The SpaceX example `spacex_example.py` is a more advanced example using this approach."""

import sys

# To run the test from this directory
sys.path.insert(0, "../..")

import cloudofficeprint as cop

import requests

SERVER_URL = "https://api.cloudofficeprint.com/"
API_KEY = "YOUR_API_KEY"  # Replace by your own API key

# Setup Cloud Office Print server
server = cop.config.Server(
    SERVER_URL,
    cop.config.ServerConfig(api_key=API_KEY),
)

# Create the main element collection that contains all data
data = cop.elements.ElementCollection()

# Get solar system data from https://api.le-systeme-solaire.net/rest/bodies/
res = requests.get("https://api.le-systeme-solaire.net/rest/bodies/")
json = res.json()

# Add the title to the data
main_title = cop.elements.Property("main_title", "The solar system")
data.add(main_title)

# Add the source for the data
data_source = cop.elements.Hyperlink(
    name="data_source",
    url="https://api.le-systeme-solaire.net/rest/bodies/",
    text="Data source",
)
data.add(data_source)

# Process data: we only want planets
planet_list = [
    cop.elements.ElementCollection.from_mapping(body)
    for body in json["bodies"]
    if body["isPlanet"]
]

planets = cop.elements.ForEach("planets", planet_list)
data.add(planets)

# Add planet radius chart to data
color = [None for _ in planet_list]
color[0] = "#7298d4"  # Specify the color for the first pie slice

radius_series = cop.elements.PieSeries(
    x=[planet["name"] for planet in planets.as_dict["planets"]],
    y=[planet["equaRadius"] for planet in planets.as_dict["planets"]],
    name="radius",
    colors=color,
)

radius_chart_options = cop.elements.ChartOptions(border=False)

radius_chart_options.set_legend(style=cop.elements.ChartTextStyle(color="black"))

radius_chart = cop.elements.Pie3DChart(
    name="planet_radius_chart",
    pies=(radius_series,),
    options=radius_chart_options,
)
data.add(radius_chart)

# Create print job
print_job = cop.PrintJob(
    data=data,
    server=server,
    template=cop.Template.from_local_file("solar_system_template.pptx"),  # pptx
    # template=cop.Resource.from_local_file("solar_system_template.docx"),  # docx
)

response = print_job.execute()
response.to_file("output")
