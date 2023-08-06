"""
"""
__docformat__ = "restructuredtext"
# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("wordcloud", "matplotlib")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

from accuasset.ds import *
from accuasset.domain import *

#__all__ = ['timeseries']