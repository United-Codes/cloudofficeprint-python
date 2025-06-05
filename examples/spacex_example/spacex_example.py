import sys

# To run the test from this directory
sys.path.insert(0, "../..")

import cloudofficeprint as cop

import requests


SERVER_URL = "https://api.cloudofficeprint.com/"
API_KEY = "YOUR_API_KEY"  # Replace by your own API key

IMAGE_MAX_HEIGHT = 250  # pptx, xlsx
IMAGE_MAX_WIDTH = 400  # pptx, xlsx
CHART_WIDTH = (800,)  # pptx, xlsx
# IMAGE_MAX_HEIGHT = 500  # docx
# IMAGE_MAX_WIDTH = 640  # docx
# CHART_WIDTH = 650  # docx

# Setup Cloud Office Print server
server = cop.config.Server(
    SERVER_URL,
    cop.config.ServerConfig(api_key=API_KEY),
)

# Create data object that contains all the data needed to fill in the template
data = cop.elements.ElementCollection()


def shorten_description(input: str) -> str:
    """Return only the first sentence of an input.

    Args:
        input (str): The input that needs to be shortened

    Returns:
        str: First sentence of input string
    """
    return input.split(".")[0] + "."


# Get SpaceX data from https://docs.spacexdata.com
info = requests.get("https://api.spacexdata.com/v3/info").json()  # v4 not supported
rockets = requests.get("https://api.spacexdata.com/v4/rockets").json()
dragons = requests.get("https://api.spacexdata.com/v4/dragons").json()
launch_pads = requests.get("https://api.spacexdata.com/v4/launchpads").json()
landing_pads = requests.get("https://api.spacexdata.com/v4/landpads").json()
ships = requests.get("https://api.spacexdata.com/v4/ships").json()


# Add data source hyperlink
data_source = cop.elements.Hyperlink(
    name="data_source",
    url="https://docs.spacexdata.com",
    text="Data source",
)
data.add(data_source)


# Add information about SpaceX
data.add_all(cop.elements.ElementCollection.from_mapping(info))

# Add SpaceX website as hyperlink
website = cop.elements.Hyperlink(
    name="spacex_website",
    url=info["links"]["website"],
    text="Website",
)
data.add(website)


# Add rocket data

# Add rockets description
rockets_description = cop.elements.Property(
    "rockets_description",
    "Data about the rockets built by SpaceX",
)
data.add(rockets_description)

# Add rocket data to a list
rocket_list = []

# Add rocket images, wikipedia hyperlink and shortened description for each rocket
for rocket in rockets:
    collec = cop.elements.ElementCollection.from_mapping(rocket)

    img = cop.elements.Image.from_url("image", rocket["flickr_images"][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    hyper = cop.elements.Hyperlink(
        name="wikipedia",
        url=rocket["wikipedia"],
        text="Wikipedia",
    )
    collec.add(hyper)

    short_description = cop.elements.Property(
        "description",
        shorten_description(rocket["description"]),
    )
    collec.add(short_description)  # Overwrites the current description

    rocket_list.append(collec)

rocket_data = cop.elements.ForEach("rockets", rocket_list)
data.add(rocket_data)

# Add rocket chart
x = [rocket["name"] for rocket in rockets]
cost_y = [rocket["cost_per_launch"] for rocket in rockets]


cost_series = cop.elements.ColumnSeries(
    x=x,
    y=cost_y,
    name="Cost per launch",
    color="#087c6c",
)

rockets_chart_options = cop.elements.ChartOptions(
    x_axis=cop.elements.ChartAxisOptions(
        title="Rocket", title_style=cop.elements.ChartTextStyle(color="black")
    ),
    y_axis=cop.elements.ChartAxisOptions(
        title="Cost ($)",
        title_rotation=-90,
        title_style=cop.elements.ChartTextStyle(color="black"),
        major_grid_lines=True,
    ),
    width=CHART_WIDTH,
    height=300,
    rounded_corners=True,
    border=False,
    background_color="#c8a45c",
    background_opacity=50,
)

rockets_chart_options.set_legend(style=cop.elements.ChartTextStyle(color="black"))

rockets_chart = cop.elements.ColumnChart(
    name="rockets_chart",
    columns=(cost_series,),
    options=rockets_chart_options,
)
data.add(rockets_chart)


# Add dragons data

# Add dragons description
dragon_description = cop.elements.Property(
    "dragons_description",
    "Data about the dragon capsules of SpaceX",
)
data.add(dragon_description)

# Add dragon data to a list
dragon_list = []

# Add dragon images, wikipedia hyperlink and shortened description for each dragon
for dragon in dragons:
    collec = cop.elements.ElementCollection.from_mapping(dragon)

    img = cop.elements.Image.from_url("image", dragon["flickr_images"][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    hyper = cop.elements.Hyperlink(
        name="wikipedia",
        url=dragon["wikipedia"],
        text="Wikipedia",
    )
    collec.add(hyper)

    short_description = cop.elements.Property(
        "description",
        shorten_description(dragon["description"]),
    )
    collec.add(short_description)  # Overwrites the current description

    dragon_list.append(collec)

dragon_data = cop.elements.ForEach("dragons", dragon_list)
data.add(dragon_data)


# Add launch pads data

# Add launch pads description
launch_pad_description = cop.elements.Property(
    "launch_pads_description",
    "Data about SpaceX's launch pads",
)
data.add(launch_pad_description)

# Add launch pad data to a list
launch_pad_list = []

# Add launch pad images, wikipedia hyperlink and shortened description for each launch_pad
for launch_pad in launch_pads:
    collec = cop.elements.ElementCollection.from_mapping(launch_pad)

    img = cop.elements.Image.from_url("image", launch_pad["images"]["large"][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    short_description = cop.elements.Property(
        "details",
        shorten_description(launch_pad["details"]),
    )
    collec.add(short_description)  # Overwrites the current description

    launch_pad_list.append(collec)

launch_pad_data = cop.elements.ForEach("launch_pads", launch_pad_list)
data.add(launch_pad_data)


# Add landing pads data

# Add landing pads description
landing_pad_description = cop.elements.Property(
    "landing_pads_description",
    "Data about SpaceX's landing pads",
)
data.add(landing_pad_description)

# Add landing pad data to a list
landing_pad_list = []

# Add landing pad images, wikipedia hyperlink and shortened description for each landing pad
for landing_pad in landing_pads:
    collec = cop.elements.ElementCollection.from_mapping(landing_pad)

    img = cop.elements.Image.from_url("image", landing_pad["images"]["large"][0])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    hyper = cop.elements.Hyperlink(
        name="wikipedia",
        url=landing_pad["wikipedia"],
        text="Wikipedia",
    )
    collec.add(hyper)

    short_description = cop.elements.Property(
        "details",
        shorten_description(landing_pad["details"]),
    )
    collec.add(short_description)  # Overwrites the current description

    landing_pad_list.append(collec)

landing_pad_data = cop.elements.ForEach("landing_pads", landing_pad_list)
data.add(landing_pad_data)


# Add ships data

# Add ships description
ship_description = cop.elements.Property(
    "ships_description",
    "Data about the ships that assist SpaceX launches, including ASDS drone ships, tugs, fairing recovery ships, and various support ships",
)
data.add(ship_description)

# Add ship data to a list
ship_list = []

# Add ship images and website hyperlink for each ship
for ship in ships:
    collec = cop.elements.ElementCollection.from_mapping(ship)

    img = cop.elements.Image.from_url("image", ship["image"])
    img.max_height = IMAGE_MAX_HEIGHT
    img.max_width = IMAGE_MAX_WIDTH
    collec.add(img)

    hyper = cop.elements.Hyperlink(
        name="website",
        url=ship["link"],
        text="Website",
    )
    collec.add(hyper)

    ship_list.append(collec)

ship_data = cop.elements.ForEach("ships", ship_list)
data.add(ship_data)


# Create print job
print_job = cop.PrintJob(
    # NOTE: change IMAGE_MAX_HEIGHT, IMAGE_MAX_WIDTH and CHART_WIDTH at the beginning of this script according to filetype
    data=data,
    server=server,
    template=cop.Template.from_local_file("spacex_template.pptx"),  # For pptx
    # template=cop.Template.from_local_file("spacex_template.xlsx"),  # For xlsx
    # template=cop.Template.from_local_file("spacex_template.docx"),  # For docx
)

response = print_job.execute()
response.to_file("output")
