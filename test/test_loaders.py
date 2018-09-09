"""This module test the loaders coming with the `abm` package."""

import sys
from types import ModuleType
from configparser import ConfigParser
from unittest import TestCase, main
from contextlib import suppress

from abm.core import HOOK_NAME, activate as activate_abm
from abm.loaders import AbmLoader, IniLoader


class TestBaseAbmLoaderClass(TestCase):
    """Check base class for abm loaders."""

    def setUp(self):
        _disable_abm()
        activate_abm()

    def test_register_without_activating(self):
        """Registering raises."""
        delattr(sys, HOOK_NAME)  # desactivate abm
        with self.assertRaises(AttributeError):
            DummyLoader.register()

    def test_register_twice(self):
        """Registering twice, raises."""
        DummyLoader.register()
        with self.assertRaises(ValueError):
            DummyLoader.register()

    def test_force_override(self):
        """Force overriding is possible."""
        DummyLoader.register()
        try:
            DummyLoader.register(override=True)
        except ValueError:
            self.fail('Can not register if passing `override` set to `True`.')

    def test_register_with_another_extension(self):
        """Registering for another extension is possible."""
        DummyLoader.register()
        DummyLoader.register(extension='.example2')
        self.assertIs(getattr(sys, HOOK_NAME)['.example2'], DummyLoader)


class TestIniLoader(TestCase):
    """Check the features of modules loaded by the `abm.loaders.IniLoader`."""

    def setUp(self):
        _disable_abm()
        activate_abm()
        IniLoader.register()

    def test_loads_a_config_file(self):
        """Loads and read a config file as a module."""
        from test.resources import config
        self.assertIsInstance(config, ModuleType)
        self.assertIsInstance(config, ConfigParser)
        self.assertIsNotNone(config['example'])
        self.assertEqual(config['example']['config-option'], 'config-value')


class DummyLoader(AbmLoader):
    extension = '.example'


def _disable_abm():
    with suppress(AttributeError):
        delattr(sys, HOOK_NAME)

if __name__ == '__main__':
    main(verbosity=2)
