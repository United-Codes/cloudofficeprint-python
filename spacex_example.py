from apexofficeprint.config import server
from apexofficeprint.resource import Resource
import apexofficeprint as aop
import requests
import pprint


# Get SpaceX data from https://docs.spacexdata.com
info = requests.get('https://api.spacexdata.com/v3/info').json() # v4 not supported
rockets = requests.get('https://api.spacexdata.com/v4/rockets').json()
dragons = requests.get('https://api.spacexdata.com/v4/dragons').json()
landing_pads = requests.get('https://api.spacexdata.com/v4/landpads').json()
ships = requests.get('https://api.spacexdata.com/v4/ships').json()


# Setup AOP server
LOCAL_SERVER_URL = "http://localhost:8010"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

server = aop.config.Server(
    LOCAL_SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)


# Create data object
data = aop.elements.ElementCollection()


# Add information about SpaceX
data.add_all(aop.elements.ElementCollection.from_mapping(info))


# Add data source
data.add(aop.elements.Hyperlink(
    name='data_source',
    url='https://docs.spacexdata.com',
    text='Data source'
))

# Add rockets description
data.add(aop.elements.Property('rockets_description', 'Data about the rockets built by SpaceX'))

# Add dragons description
data.add(aop.elements.Property('dragons_description', 'Data about the dragon capsules of SpaceX'))

# Add landing pads description
data.add(aop.elements.Property('landing_pads_description', "Data about SpaceX's landing pads"))

# Add ships description
data.add(aop.elements.Property('ships_description', 'Data about the ships that assist SpaceX launches, including ASDS drone ships, tugs, fairing recovery ships, and various support ships'))


# Add rocket data
## Add rocket images
for i in range(len(rockets)):
    img = aop.elements.Image.from_url('image', rockets[i]['flickr_images'][0])
    img.max_height = 250
    img.max_width = 400
    rockets[i].update(img.as_dict)


rocket_list = [aop.elements.ElementCollection.from_mapping(rocket) for rocket in rockets]
rocket_data = aop.elements.ForEach('rockets', rocket_list)
data.add(rocket_data)

# Add dragons data
## Add dragon images
for i in range(len(dragons)):
    img = aop.elements.Image.from_url('image', dragons[i]['flickr_images'][0])
    img.max_height = 250
    img.max_width = 400
    dragons[i].update(img.as_dict)

dragon_list = [aop.elements.ElementCollection.from_mapping(dragon) for dragon in dragons]
dragon_data = aop.elements.ForEach('dragons', dragon_list)
data.add(dragon_data)

# Add landing pads data
## Add landing pad images
for i in range(len(landing_pads)):
    img = aop.elements.Image.from_url('image', landing_pads[i]['images']['large'][0])
    img.max_height = 250
    img.max_width = 400
    landing_pads[i].update(img.as_dict)
    # Preprocess details (only take first sentence of description)
    landing_pads[i]['details'] = landing_pads[i]['details'].split('.')[0] + '.'

## Add landing pads data
landing_pad_list = [aop.elements.ElementCollection.from_mapping(landing_pad) for landing_pad in landing_pads]
landing_pad_data = aop.elements.ForEach('landing_pads', landing_pad_list)

data.add(landing_pad_data)

# Add ships data
## Add ship images
for i in range(len(ships)):
    img = aop.elements.Image.from_url('image', ships[i]['image'])
    img.max_height = 250
    img.max_width = 400
    ships[i].update(img.as_dict)

ship_list = [aop.elements.ElementCollection.from_mapping(ship) for ship in ships]
ship_data = aop.elements.ForEach('ships', ship_list)
data.add(ship_data)


# Create printjob
printjob = aop.PrintJob(
    template=Resource.from_local_file('./spacex_example/spacex_template.pptx'),
    data=data,
    server=server
)

printjob.execute().to_file('./spacex_example/output')
