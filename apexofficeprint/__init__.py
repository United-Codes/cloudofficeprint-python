"""
This Python package provides a programmatic interface with an [APEX Office Print](https://www.apexofficeprint.com) server.

## Example
```python
# TODO: the example should go here
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
