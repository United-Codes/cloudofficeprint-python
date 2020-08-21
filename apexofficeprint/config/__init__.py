"""
Module for output configurations.

The classes under this module encapsulate various configuration options for a print job.
They are to be used with `apexofficeprint.printjob.PrintJob`.
"""

from .cloud import *
from .output import OutputConfig
from .pdf import *
from .server import Server, ServerConfig
