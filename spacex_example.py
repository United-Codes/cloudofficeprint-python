import apexofficeprint as aop
import requests


# Setup AOP server
LOCAL_SERVER_URL = "http://localhost:8010"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

server = aop.config.Server(
    LOCAL_SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)


# Create data object that contains all the data needed to fill in the template
data = aop.elements.ElementCollection()


def shorten_description(input: str) -> str:
    """Return only the first sentence of an input.

    Args:
        input (str): The input that needs to be shortened

    Returns:
        str: First sentence of input string
    """
    return input.split('.')[0] + '.'


# IMAGE_MAX_HEIGHT = 250  # pptx, xlsx
# IMAGE_MAX_WIDTH = 400  # pptx, xlsx
IMAGE_MAX_HEIGHT = 500  # docx
IMAGE_MAX_WIDTH = 640  # docx


# Get SpaceX data from https://docs.spacexdata.com
info = requests.get('https://api.spacexdata.com/v3/info').json() # v4 not supported
rockets = requests.get('https://api.spacexdata.com/v4/rockets').json()
dragons = requests.get('https://api.spacexdata.com/v4/dragons').json()
launch_pads = requests.get('https://api.spacexdata.com/v4/launchpads').json()
landing_pads = requests.get('https://api.spacexdata.com/v4/landpads').json()
ships = requests.get('https://api.spacexdata.com/v4/ships').json()


# Add data source hyperlink
data_source = aop.elements.Hyperlink(
    name='data_source',
    url='https://docs.spacexdata.com',
    text='Data source'
)
data.add(data_source)


# Add information about SpaceX
data.add_all(aop.elements.ElementCollection.from_mapping(info))

## Add SpaceX website as hyperlink
website = aop.elements.Hyperlink(
    name='spacex_website',
    url=info['links']['website'],
    text='Website'
)
data.add(website)


# Add rocket data
## Add rockets description
rockets_description = aop.elements.Property('rockets_description', 'Data about the rockets built by SpaceX')
data.add(rockets_description)

## Add rocket data to a list
rocket_list = []

## Add rocket images, wikipedia hyperlink and shortened description for each rocket
for rocket in rockets:
    collec = aop.elements.ElementCollection.from_mapping(rocket)

    img = aop.elements.Image.from_url('image', rocket['flickr_images'][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    hyper = aop.elements.Hyperlink(
        name='wikipedia',
        url=rocket['wikipedia'],
        text='Wikipedia'
    )
    collec.add(hyper)

    short_description = aop.elements.Property('description', shorten_description(rocket['description']))
    collec.add(short_description)  # Overwrites the current description

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
    name='Cost per launch',
    color='#087c6c'
)

rockets_chart_options = aop.elements.ChartOptions(
    x_axis=aop.elements.ChartAxisOptions(
        title='Rocket',
        title_style=aop.elements.ChartTextStyle(color='black')
    ),
    y_axis=aop.elements.ChartAxisOptions(
        title='Cost ($)',
        title_rotation=-90,
        title_style=aop.elements.ChartTextStyle(color='black'),
        major_grid_lines=True
    ),
    # width=800,  # pptx and xlsx
    width=650,  # docx
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
## Add dragons description
data.add(aop.elements.Property('dragons_description', 'Data about the dragon capsules of SpaceX'))

## Add dragon data to a list
dragon_list = []

## Add dragon images, wikipedia hyperlink and shortened description for each dragon
for dragon in dragons:
    collec = aop.elements.ElementCollection.from_mapping(dragon)
    
    img = aop.elements.Image.from_url('image', dragon['flickr_images'][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    hyper = aop.elements.Hyperlink(
        name='wikipedia',
        url=dragon['wikipedia'],
        text='Wikipedia'
    )
    collec.add(hyper)

    short_description = aop.elements.Property('description', shorten_description(dragon['description']))
    collec.add(short_description)  # Overwrites the current description

    dragon_list.append(collec)

dragon_data = aop.elements.ForEach('dragons', dragon_list)
data.add(dragon_data)


# Add launch pads data
## Add launch pads description
data.add(aop.elements.Property('launch_pads_description', "Data about SpaceX's launch pads"))

## Add launch pad data to a list
launch_pad_list = []

## Add launch pad images, wikipedia hyperlink and shortened description for each launch_pad
for launch_pad in launch_pads:
    collec = aop.elements.ElementCollection.from_mapping(launch_pad)
    
    img = aop.elements.Image.from_url('image', launch_pad['images']['large'][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    short_description = aop.elements.Property('details', shorten_description(launch_pad['details']))
    collec.add(short_description)  # Overwrites the current description

    launch_pad_list.append(collec)

launch_pad_data = aop.elements.ForEach('launch_pads', launch_pad_list)
data.add(launch_pad_data)


# Add landing pads data
## Add landing pads description
data.add(aop.elements.Property('landing_pads_description', "Data about SpaceX's landing pads"))

## Add landing pad data to a list
landing_pad_list = []

## Add landing pad images, wikipedia hyperlink and shortened description for each landing pad
for landing_pad in landing_pads:
    collec = aop.elements.ElementCollection.from_mapping(landing_pad)
    
    img = aop.elements.Image.from_url('image', landing_pad['images']['large'][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    hyper = aop.elements.Hyperlink(
        name='wikipedia',
        url=landing_pad['wikipedia'],
        text='Wikipedia'
    )
    collec.add(hyper)

    short_description = aop.elements.Property('details', shorten_description(landing_pad['details']))
    collec.add(short_description)  # Overwrites the current description

    landing_pad_list.append(collec)

landing_pad_data = aop.elements.ForEach('landing_pads', landing_pad_list)

data.add(landing_pad_data)


# Add ships data
## Add ships description
data.add(aop.elements.Property('ships_description', 'Data about the ships that assist SpaceX launches, including ASDS drone ships, tugs, fairing recovery ships, and various support ships'))

## Add ship data to a list
ship_list = []

## Add ship images and website hyperlink for each ship
for ship in ships:
    collec = aop.elements.ElementCollection.from_mapping(ship)
    
    img = aop.elements.Image.from_url('image', ship['image'])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

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
    # template=aop.Resource.from_local_file('./examples/spacex_example/spacex_template.pptx'), # For pptx
    # template=aop.Resource.from_local_file('./examples/spacex_example/spacex_template.xlsx'), # For xlsx
    template=aop.Resource.from_local_file('./examples/spacex_example/spacex_template.docx'), # For docx
    data=data,
    server=server
)

printjob.execute().to_file('./examples/spacex_example/output')
