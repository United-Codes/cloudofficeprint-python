"""
This Python package provides a programmatic interface with an APEX Office print server.

# Example
TODO: include test.py as an example (as example.py)?

"""

# These classes are in separate files, but should be exposed directly in this module.
# For example, we want apexofficeprint.PrintJob instead of apexofficeprint.printjob.PrintJob.
from .resource import Resource
from .printjob import PrintJob
from .response import Response

# Add exceptions for pdoc to those modules whose content is exposed here.
__pdoc__ = {
    "printjob": False,
    "resource": False,
    "response": False
}

# specify what is imported on "from apexofficeprint import *"
# but that shouldn't really be used anyway
__all__ = [
    "Resource",
    "PrintJob",
    "Response",
    "exceptions",
    "config"
]
