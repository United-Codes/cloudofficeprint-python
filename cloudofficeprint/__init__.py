"""
This Python package provides a programmatic interface with a [Cloud Office Print](https://www.cloudofficeprint.com) server.

## Usage
The examples below call this package cop.
```python
import cloudofficeprint as cop
```

### Templates
Templates are represented by `Resource`. The simplest way to obtain a `Resource` is to load from a local path.
```python
template = cop.Resource.from_local_file("./path/to/template.docx")
```

### Render elements
Most render elements encapsulate the data for a single tag. An `elements.ElementCollection` is an element which represents a collection of elements.

Combining a simple line chart and some text tags:
```python
line = cop.elements.LineChart(
    "linechart",
    cop.elements.LineSeries([1, 2, 3, 4], [1, 2, 3, 4], color="green"),
    cop.elements.XYSeries([1, 2, 3, 4], ["a", "b", "c", "d"])
)

text_tag = cop.elements.Property("tag-name", "Hello, world!")
# or multiple at once using ElementCollection.from_mapping
# and supplying the dictionary representation directly
text_tags = cop.elements.ElementCollection.from_mapping({
    "another-tag": "Foo",
    "one-more-tag": "Bar"
})

combined_data = cop.elements.ElementCollection()
combined_data.add(line)
combined_data.add(text_tag)
combined_data.add_all(text_tags)
```

### The server
A Cloud Office Print server is configured as a `config.Server`. It takes a url and an optional `config.ServerConfig` which allows for various server configuration options. If you're using Cloud Office Print Cloud edition, you will need to use this to declare your API key.

```python
server = cop.config.Server(
    "http://server.url.com/",
    cop.config.ServerConfig(api_key = "YOUR_API_KEY")
)
```

### Print job
`PrintJob` combines template, data, server and an optional output configuration (`config.OutputConfig`) and can execute itself on the Cloud Office Print server. An example using the variables declared above:

```python
printjob = cop.PrintJob(combined_data, server, template)
printjob.execute()
```

A print job can be executed asynchronously as well.

```python
import asyncio
coroutine = printjob.execute_async()
# simply await your result when you need it
result = await coroutine
```

### Full JSON available
If you already have the JSON to be sent to the server (not just the data, but the entire JSON body including your API key and template), this package will wrap the request to the server for you (requests are made using [requests](https://requests.readthedocs.io/en/master/)).
```python
json_data = open("./path/to/data.json", "r").read()
cop.PrintJob.execute_full_json(
        json_data, server
    ).to_file("./test/from_full_json_output")
```

### Server errors
In case the Cloud Office Print server returns an error, `PrintJob` will throw one as well.
You can catch it and get either its user-readable message or an encoded stack trace that can be passed to Cloud Office Print support.
```python
try:
    # execute some previously constructed printjob
    printjob.execute()
except cop.exceptions.COPError as err:
    print("Cloud Office Print error! " + err.user_message)
    print(err.encoded_message)
    ...
```

### Further information
For further information, such as where to find our examples, we refer to our README.md file on our [Github page](https://github.com/United-Codes/cloudofficeprint-python/).
"""

from . import exceptions, config, elements, own_utils

from .printjob import PrintJob
from .resource import Resource
from .response import Response

# specify what is imported on "from cloudofficeprint import *"
# but that shouldn't really be used anyway
__all__ = [
    "exceptions",
    "config",
    "elements",
    "own_utils",
    "PrintJob",
    "Resource",
    "Response"
]
