"""A collection of loaders for handling typical extensions."""

import sys
import json
from collections import MutableMapping, MutableSequence
from types import ModuleType
from configparser import ConfigParser
from importlib._bootstrap import _init_module_attrs
from importlib.abc import Loader
from abm.core import HOOK_NAME


class AbmLoader(Loader):
    """Base class for helping implement loaders for non-python files."""

    @classmethod
    def init_module_attrs(cls, spec, module):
        return _init_module_attrs(spec, module)

    @classmethod
    def register(cls, extensions=None, override=False):
        if not hasattr(sys, HOOK_NAME):
            raise AttributeError('sys.{} is not present, ensure you have'
                                 'enabled abm by importing `activate`.'
                                 .format(HOOK_NAME))

        extensions = extensions or cls.extensions
        for extension in extensions:
            if not override and extension in sys.abm_hooks:
                raise ValueError('Cannot set register this loader for '
                                 'extension "{}". It is already in use.'
                                 .format(extension))
            sys.abm_hooks[extension] = cls


class IniLoader(AbmLoader):
    """Load .ini config files as modules. Modules imported via this loader are
    instances both of ``ModuleType`` and ``ConfigParser``."""

    extensions = ('.ini', )

    def __init__(self, name, path):
        self.module_name = name
        self.file_path = path

    def exec_module(self, module):
        module.read(self.file_path)
        return module

    def create_module(self, spec):
        module = ConfigModule(spec.name)
        self.init_module_attrs(spec, module)
        return module


class ConfigModule(ModuleType, ConfigParser):
    """Represent both a module and a configuration ini file. All methods of
    ``configparser.ConfigParser`` are available for the instances of this
    class."""

    def __init__(self, specname):
        ModuleType.__init__(self, specname)
        ConfigParser.__init__(self)


class JsonLoader(AbmLoader):
    """Load .json files as modules. Modules imported via this loader are
    instances of ``ModuleType``, ``MutableMapping`` and ``MutableSequence``
    and so, they can be accessed in the same way you would access dictionaries
    or lists."""

    extensions = ('.json', )

    def __init__(self, name, path):
        self.file_path = path

    def create_module(self, spec):
        module = JsonModule(spec.name)
        self.init_module_attrs(spec, module)
        return module

    def exec_module(self, module):
        with open(self.file_path) as jsonfile:
            data = json.load(jsonfile)
        module._data = data
        return module


class JsonModule(ModuleType, MutableSequence, MutableMapping):
    """Represent both a module and a JSON object. Instances of this classes
    are mutable mappings and mutable sequences."""

    def __init__(self, specname):
        ModuleType.__init__(self, specname)
        self._data = None

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def insert(self, position, value):
        return self._data.insert(position, value)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)
