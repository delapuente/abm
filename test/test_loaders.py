"""This module test the loaders coming with the `abm` package."""

import sys
from types import ModuleType
from configparser import ConfigParser
from unittest import TestCase, main
from contextlib import suppress

from abm.core import HOOK_NAME, activate as activate_abm
from abm.loaders import AbmLoader, IniLoader, JsonLoader


class TestBaseAbmLoaderClass(TestCase):
    """Check base class for abm loaders."""

    def setUp(self):
        _disable_abm()
        activate_abm()

    def test_register_without_activating(self):
        """Registering raises."""
        delattr(sys, HOOK_NAME)  # deactivate abm
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
        DummyLoader.register(extensions=('.example2', ))
        self.assertIs(getattr(sys, HOOK_NAME)['.example2'], DummyLoader)


class TestIniLoader(TestCase):
    """Check the features of modules loaded by the
    ``abm.loaders.IniLoader`` loader."""

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


class TestJsonLoader(TestCase):
    """Check the features of modules loaded by the
    ``abm.loaders.JsonLoader`` loader."""

    def setUp(self):
        _disable_abm()
        activate_abm()
        JsonLoader.register()

    def test_loads_a_non_object_json_file(self):
        """The data will be available through the ``_data`` member."""
        from test.resources import simple_json
        self.assertEqual(simple_json._data, 'test')

    def test_loads_an_array_json_file(self):
        """The data will be available through the ``_data`` and the
        module can be accessed as a mutable sequence."""
        from test.resources import array_json
        self.assertEqual(array_json._data, [1, 2, 3])
        self.assertEqual(len(array_json), 3)
        self.assertEqual(array_json[0], 1)

    def test_load_an_object_json_file(self):
        """The data will be available through the ``_data`` and the
        module can be accessed as a mutable map."""
        from test.resources import object_json
        self.assertEqual(object_json._data, {'answer': 42})
        self.assertEqual(len(object_json), 1)
        self.assertEqual(object_json['answer'], 42)


class DummyLoader(AbmLoader):
    extensions = ('.example', )


def _disable_abm():
    with suppress(AttributeError):
        delattr(sys, HOOK_NAME)

if __name__ == '__main__':
    main(verbosity=2)
