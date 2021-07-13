from apexofficeprint.config import server
from apexofficeprint.resource import Resource
import apexofficeprint as aop
import requests


# Get SpaceX data from https://docs.spacexdata.com
info = requests.get('https://api.spacexdata.com/v3/info').json() # v4 not supported
rockets = requests.get('https://api.spacexdata.com/v4/rockets').json()
dragons = requests.get('https://api.spacexdata.com/v4/dragons').json()
launch_pads = requests.get('https://api.spacexdata.com/v4/launchpads').json()
landing_pads = requests.get('https://api.spacexdata.com/v4/landpads').json()
ships = requests.get('https://api.spacexdata.com/v4/ships').json()


# Setup AOP server
LOCAL_SERVER_URL = "http://localhost:8010"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

server = aop.config.Server(
    LOCAL_SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)


# Create data object that contains all the data needed to fill in the template
data = aop.elements.ElementCollection()


# Add information about SpaceX
data.add_all(aop.elements.ElementCollection.from_mapping(info))

## Add SpaceX website as hyperlink
website = aop.elements.Hyperlink(
    name='spacex_website',
    url=info['links']['website'],
    text='Website'
)
data.add(website)


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

# Add launch pads description
data.add(aop.elements.Property('launch_pads_description', "Data about SpaceX's launch pads"))

# Add landing pads description
data.add(aop.elements.Property('landing_pads_description', "Data about SpaceX's landing pads"))

# Add ships description
data.add(aop.elements.Property('ships_description', 'Data about the ships that assist SpaceX launches, including ASDS drone ships, tugs, fairing recovery ships, and various support ships'))


def shorten_description(input: str) -> str:
    """Return only the first sentence of an input.

    Args:
        input (str): The input that needs to be shortened

    Returns:
        str: First sentence of input string
    """
    return input.split('.')[0] + '.'


# Add rocket data
## Add rocket images and shorten description
for i in range(len(rockets)):
    img = aop.elements.Image.from_url('image', rockets[i]['flickr_images'][0])
    img.max_height = 250
    img.max_width = 400
    rockets[i].update(img.as_dict)
    rockets[i]['description'] = shorten_description(rockets[i]['description'])


## Add rocket data to a list
rocket_list = []

## Add wikipedia hyperlink for each rocket
for rocket in rockets:
    collec = aop.elements.ElementCollection.from_mapping(rocket)
    hyper = aop.elements.Hyperlink(
        name='wikipedia',
        url=rocket['wikipedia'],
        text='Wikipedia'
    )
    collec.add(hyper)
    rocket_list.append(collec)

rocket_data = aop.elements.ForEach('rockets', rocket_list)
data.add(rocket_data)

## Add rocket chart
x = []
cost_y = []

for rocket in rockets:
    x.append(rocket['name'])
    cost_y.append(rocket['cost_per_launch'])

cost_series = aop.elements.ColumnSeries(
    x=x,
    y=cost_y,
    name='Cost per launch'
)

rockets_chart_options = aop.elements.ChartOptions(
    x_axis=aop.elements.ChartAxisOptions(
        title='Rocket',
        title_style=aop.elements.ChartTextStyle(color='black')
    ),
    y_axis=aop.elements.ChartAxisOptions(
        title='Cost ($)',
        title_rotation=-90,
        title_style=aop.elements.ChartTextStyle(color='black')
    ),
    width=800,
    height=300,
    rounded_corners=True,
    border=False,
    background_color='#c8a45c',
    background_opacity=50
)

rockets_chart_options.set_legend(
    style=aop.elements.ChartTextStyle(color='black')
)

rockets_chart = aop.elements.ColumnChart(
    name='rockets_chart',
    columns=(cost_series,),
    options=rockets_chart_options
)

data.add(rockets_chart)


# Add dragons data
## Add dragon images and shorten description
for i in range(len(dragons)):
    img = aop.elements.Image.from_url('image', dragons[i]['flickr_images'][0])
    img.max_height = 250
    img.max_width = 400
    dragons[i].update(img.as_dict)
    dragons[i]['description'] = shorten_description(dragons[i]['description'])

## Add dragon data to a list
dragon_list = []

## Add wikipedia hyperlink for each dragon
for dragon in dragons:
    collec = aop.elements.ElementCollection.from_mapping(dragon)
    hyper = aop.elements.Hyperlink(
        name='wikipedia',
        url=dragon['wikipedia'],
        text='Wikipedia'
    )
    collec.add(hyper)
    dragon_list.append(collec)

dragon_data = aop.elements.ForEach('dragons', dragon_list)
data.add(dragon_data)

# Add launch pads data
## Add launch pad images and shorten description
for i in range(len(launch_pads)):
    img = aop.elements.Image.from_url('image', launch_pads[i]['images']['large'][0])
    img.max_height = 250
    img.max_width = 400
    launch_pads[i].update(img.as_dict)
    launch_pads[i]['details'] = shorten_description(launch_pads[i]['details'])

## Add launch pads data
launch_pad_list = [aop.elements.ElementCollection.from_mapping(launch_pad) for launch_pad in launch_pads]
launch_pad_data = aop.elements.ForEach('launch_pads', launch_pad_list)

data.add(launch_pad_data)

# Add landing pads data
## Add landing pad images and shorten description
for i in range(len(landing_pads)):
    img = aop.elements.Image.from_url('image', landing_pads[i]['images']['large'][0])
    img.max_height = 250
    img.max_width = 400
    landing_pads[i].update(img.as_dict)
    landing_pads[i]['details'] = shorten_description(landing_pads[i]['details'])

## Add landing_pad data to a list
landing_pad_list = []

## Add wikipedia hyperlink for each landing_pad
for landing_pad in landing_pads:
    collec = aop.elements.ElementCollection.from_mapping(landing_pad)
    hyper = aop.elements.Hyperlink(
        name='wikipedia',
        url=landing_pad['wikipedia'],
        text='Wikipedia'
    )
    collec.add(hyper)
    landing_pad_list.append(collec)

landing_pad_data = aop.elements.ForEach('landing_pads', landing_pad_list)

data.add(landing_pad_data)

# Add ships data
## Add ship images
for i in range(len(ships)):
    img = aop.elements.Image.from_url('image', ships[i]['image'])
    img.max_height = 250
    img.max_width = 400
    ships[i].update(img.as_dict)

## Add ship data to a list
ship_list = []

## Add wikipedia hyperlink for each ship
for ship in ships:
    collec = aop.elements.ElementCollection.from_mapping(ship)
    hyper = aop.elements.Hyperlink(
        name='website',
        url=ship['link'],
        text='Website'
    )
    collec.add(hyper)
    ship_list.append(collec)

ship_data = aop.elements.ForEach('ships', ship_list)
data.add(ship_data)


# Create printjob
printjob = aop.PrintJob(
    template=Resource.from_local_file('./spacex_example/spacex_template.pptx'),
    data=data,
    server=server
)

printjob.execute().to_file('./spacex_example/output')
