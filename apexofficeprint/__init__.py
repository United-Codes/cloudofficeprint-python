"""
This Python package provides a programmatic interface with an [APEX Office Print](https://www.apexofficeprint.com) server.

## Examples
The examples below call this package aop.
```python
import apexofficeprint as aop
```

### Templates
Templates are represented by `Resource`. The simplest way to obtain a `Resource` is to load from a local path.
```python
template = aop.Resource.from_local_file("./path/to/template.docx")
```

### Render elements
Most render elements encapsulate the data for a single tag. An `elements.Object` is an element which represents a collection of elements.

Combining a simple line chart and some text tags:
```python
line = aop.elements.LineChart(
    "linechart",
    aop.elements.LineSeries([1, 2, 3, 4], [1, 2, 3, 4], color="green"),
    aop.elements.XYSeries([1, 2, 3, 4], ["a", "b", "c", "d"])
)

text_tag = aop.elements.Property("tag-name", "Hello, world!")
# or multiple at once using Object.from_mapping
# and supplying the dictionary representation directly
text_tags = aop.elements.Object.from_mapping({
    "another-tag": "Foo",
    "one-more-tag": "Bar"
})

combined_data = aop.elements.Object()
combined_data.add(line)
combined_data.add(text_tag)
combined_data.add_all(text_tags)
```

### The server
An AOP server is configured as a `config.Server`. It takes an url and an optional `config.ServerConfig` which allows for various server configuration options. If you're using APEX Office Print Cloud edition, you will need to use this to declare your API key.

```python
server = aop.config.Server(
    "http://server.url.com/",
    aop.config.ServerConfig(api_key = "YOUR_API_KEY")
)
```

### Print job
`PrintJob` combines template, data, server and an optional output configuration (`config.OutputConfig`) and can execute itself on the AOP server. An example using the variables declared throughout the previous examples.

```python
printjob = aop.PrintJob(template, combined_data, server)
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
aop.PrintJob.execute_full_json(
        json_data, server
    ).to_file("./test/from_full_json_output")
```

### Server errors
In case the AOP server returns an error, `PrintJob` will throw one as well.
You can catch it and get either its user-readable message or an encoded stack trace that can be passed to AOP support.
```python
try:
    # execute some previously constructed printjob
    printjob.execute()
except aop.exceptions.AOPError as err:
    print("AOP error! " + err.user_message)
    print(err.encoded_message)
    ...
```
"""

from . import exceptions, config, elements

from .printjob import PrintJob
from .resource import Resource
from .response import Response

# specify what is imported on "from apexofficeprint import *"
# but that shouldn't really be used anyway
__all__ = [
    "exceptions",
    "config",
    "elements",
    "PrintJob",
    "Resource",
    "Response"
]
