"""Contains the utilities to extend the import machinery and provide support
for ``abm``.

Extension mechanism work by monkeypatching the ``FileFinder`` class in charge
of reading Python several format modules from the local file system.

Internally, ``FileFinder`` uses file loaders to read the several formats of
Python modules identified by their file extension. Although these classes are
public, ``FileFinder`` does not expose any extension mechanism to link new
extensions with new loaders.

In the spirit of ``sys.path_hooks`` and other extension hooks, activating
``abm`` will expose a dictionary in ``sys.abm_hooks`` to register new loaders
dynamically. For instance::

    import sys
    from abm.loaders import IniLoader
    from abm.core import activate

    activate()
    sys.abm_hooks['.ini'] = IniLoader

It works by turning the internal instance attribute ``_loaders`` of
``FileFinder`` instances into a class property. Setting the property will
diverge the new value to a different attribute while reading the value will
combine the original one with the extensions in ``sys.abm_hooks``.
"""

import sys
from importlib.machinery import FileFinder
from itertools import chain

"""The name of the property in ``sys`` used to expose ``_ABM_HOOKS``."""
HOOK_NAME = 'abm_hooks'


def _set_loaders(self, loaders):
    self._builtin_loaders = loaders


def _get_loaders(self):
    return chain(self._builtin_loaders, getattr(sys, HOOK_NAME).items())


def activate():
    """Enable abm support through ``sys.abm_hooks``."""
    if not hasattr(sys, HOOK_NAME):
        setattr(sys, HOOK_NAME, {})
        FileFinder._loaders = property(_get_loaders, _set_loaders)
        sys.path_importer_cache.clear()
