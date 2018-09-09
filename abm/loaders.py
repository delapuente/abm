"""A collection of loaders for handling typical extensions."""

import sys
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
    def register(cls, extension=None, override=False):
        extension = extension or cls.extension
        if not hasattr(sys, HOOK_NAME):
            raise AttributeError('sys.{} is not present, ensure you have'
                                 'enabled abm by importing '
                                 '`activate`.'.format(HOOK_NAME))
        if not override and extension in sys.abm_hooks:
            raise ValueError('Cannot set register this loader for extension '
                             '"{}". It is already in use.'.format(extension))
        sys.abm_hooks[extension or cls.extension] = cls


class IniLoader(AbmLoader):
    """Load .ini config files as modules. Modules imported via this loader are
    instances both of ``ModuleType`` and ``ConfigParser``."""

    extension = '.ini'

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
