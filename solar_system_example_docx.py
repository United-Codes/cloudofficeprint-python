from apexofficeprint.elements.charts import ChartAxisOptions
import apexofficeprint as aop
import requests

# Get solar system data from https://api.le-systeme-solaire.net/rest/bodies/
res = requests.get('https://api.le-systeme-solaire.net/rest/bodies/')
bodies = res.json()['bodies']


# Setup AOP server
SERVER_URL = "http://apexofficeprint.com/dev/"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

server = aop.config.Server(
    SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)


# Create data to fill template
data = aop.elements.ElementCollection.from_json(res.text)


# Add planet radius chart to data
color = [None for body in bodies]
color[0] = 'blue'

radius_series = aop.elements.PieSeries(
    x=[body['name'] for body in bodies if body['isPlanet']],
    y=[body['meanRadius'] for body in bodies if body['isPlanet']],
    name='Mass',
    colors=color
)
radius_chart_options = aop.elements.ChartOptions(
    x_axis=ChartAxisOptions(),
    y_axis=ChartAxisOptions(),
    border=False
)
radius_chart = aop.elements.Pie3DChart(
    name='planet_radius_chart',
    pies=(radius_series,)
)
data.add(radius_chart)

# Create AOP printjob
printjob = aop.PrintJob(
    template=aop.Resource.from_local_file('./examples/solar_system_example/docx/solar_system_template.docx'),
    data=data,
    server=server,
    output_config=aop.config.OutputConfig(filetype='docx')
)

printjob.execute().to_file('./examples/solar_system_example/docx/output')
