import pytest
import glib
from textscript.ConfigUtils import Setup, Update
from textscript import Logger


"""
SETUP
"""

# Get current version
text_script_version = glib.get_version()

# Initialize Logger
L = Logger()

L.log.debug(f"Automated test for: {text_script_version}")

setup = Setup(L, text_script_version)


"""
TESTING FOR: textscript.ConfigUtils.Setup
"""

