import apexofficeprint as aop

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

data.add(aop.elements.Property('main_title', 'The solar system'))


# Create printjob
printjob = aop.PrintJob(
    template=aop.Resource.from_local_file('./examples/solar_system_example/pptx/solar_system_template.pptx'),
    data=data,
    server=server
)
printjob.execute().to_file('./examples/solar_system_example/pptx/output')
