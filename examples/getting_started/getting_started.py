import sys

# To run the test from this directory
sys.path.insert(0, "../..")

import cloudofficeprint as cop

SERVER_URL = "https://api.cloudofficeprint.com/"
API_KEY = "C82C46C54A843F6FE055043998A2C4EE"  # Replace by your own API key

# Setup Cloud Office Print server
server = cop.config.Server(
    SERVER_URL,
    cop.config.ServerConfig(api_key=API_KEY),
)

# Main object that holds the data
collection = cop.elements.ElementCollection()

# Create the title element and add it to the element collection
title = cop.elements.Property(name="title", value="Hello World!")
collection.add(title)

# Create the text element and add it to the element collection
text = cop.elements.Property(
    name="text",
    value="This is an example created with the Cloud Office Print Python SDK",
)
collection.add(text)

# Create print job
print_job = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Template.from_local_file("getting_started.docx"),
)

# Execute print job and save response to file
response = print_job.execute()
response.to_file("output")
