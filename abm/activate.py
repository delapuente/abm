"""This module monkeypatches the ``importlib.machinery.FileFinder`` class to
support treating non module files as modules.

It hijacks the `_loaders` instance attribute turning it into a class property.
Setting the property is deferred to a different attribute while reading it
combines the original list with the values from the ``_LOADERS_HOOKS``
dictionary.
"""
from abm.core import activate
activate()
