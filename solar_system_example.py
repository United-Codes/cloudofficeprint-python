"""This is a standard example of how to use an API to get data to fill in a template.
The SpaceX example `spacex_example.py` is a more advanced example using this approach."""

import apexofficeprint as aop
import requests

# Get solar system data from https://api.le-systeme-solaire.net/rest/bodies/
res = requests.get('https://api.le-systeme-solaire.net/rest/bodies/').json()

# Setup AOP server
SERVER_URL = "https://api.apexofficeprint.com/"
API_KEY = "YOUR_API_KEY"  # Replace by your own API key

server = aop.config.Server(
    SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)

# Create the main element collection that contains all data
data = aop.elements.ElementCollection()

# Add the title to the data
data.add(aop.elements.Property('main_title', 'The solar system'))

# Add the source for the data
data.add(aop.elements.Hyperlink(
    name='data_source',
    url='https://api.le-systeme-solaire.net/rest/bodies/',
    text='Data source'
))

# Process data: we only want planets
planet_list = []

for body in res['bodies']:
    if body['isPlanet']:
        collec = aop.elements.ElementCollection.from_mapping(body)

        planet_list.append(collec)

planets = aop.elements.ForEach('planets', planet_list)
data.add(planets)

# Add planet radius chart to data
color = [None for _ in planet_list]
color[0] = '#7298d4'

radius_series = aop.elements.PieSeries(
    x=[planet['name'] for planet in planets.as_dict['planets']],
    y=[planet['meanRadius'] for planet in planets.as_dict['planets']],
    name='radius',
    colors=color
)

radius_chart_options = aop.elements.ChartOptions(
    border=False
)

radius_chart_options.set_legend(
    style=aop.elements.ChartTextStyle(
        color='black'
    )
)

radius_chart = aop.elements.Pie3DChart(
    name='planet_radius_chart',
    pies=(radius_series,),
    options=radius_chart_options
)
data.add(radius_chart)

# Create printjob
printjob = aop.PrintJob(
    data=data,
    server=server,
    template=aop.Resource.from_local_file('./examples/solar_system_example/pptx/solar_system_template.pptx'),  # pptx
    # template=aop.Resource.from_local_file('./examples/solar_system_example/docx/solar_system_template.docx'),  # docx
)
printjob.execute().to_file('./examples/solar_system_example/pptx/output')
# printjob.execute().to_file('./examples/solar_system_example/docx/output')
