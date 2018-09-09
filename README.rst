``abm`` - Abstract modules
==========================

> Allow loading non Python module formats as modules.

Install
-------

Use ``pip`` for installing:

.. code-block:: bash

    $ pip install abm

Usage
-----

Once installed, you can activate ``abm`` by importing ``abm.activate``::

    from abm import activate

Finally, you can register new loaders by doing::

    from abm.loaders import IniLoader
    IniLoader.register()

Now you can load ``*.ini`` files as if they were modules:

.. code-block:: ini

    # config.ini
    [section]
    option = value

.. code-block:: python

    import config
    assert(config['example'] is not None)
    assert(config['example']['opton'] is 'value')

.. note:: ``abm.loaders`` package is work in progress.
   The ``abm.loaders`` package is still work in progress and it will gather
   a set of useful loaders for common extensions.


Writing a loader
----------------

Extend the base loader ``AbmLoader`` provided in ``abm.loaders`` and implement
``create_module`` and ``execute_module`` methods. Provide the ``extension``
class member to allow automatic registration::

    import json
    from types import ModuleType
    from abm.loaders import AbmLoader


    class JsonLoader(AbmLoader):

        extension = '.json'

        deg __init__(self, name, path):
            self.file_path = path

        def create_module(self, spec)
            module = JsonModule(spec.name)
            self.init_module_attrs(spec, module)
            return module

        def execute_module(self, module):
            module.clear()
            module.update(json.load(open(self.file_path)))
            return module


    class JsonModule(ModuleType, dict):

        def __init__(self, specname):
            ModuleType.__init__(self, specname)
            dict.__init__(self)


Loaders are initialized passing the name of the module in the form::

    'path.to.the.module'

And its absolute path.

Remember registering the loader with::

    JsonLoader.register()

After activating ``amb``.

Implementing ``create_module``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``create_module`` function should produce a module of the correct type. Nothing
more. This method is passed with the module specification object used to find
the module.

A good pattern is to create a new type of module combining the functionality
of Python default modules and your specific needs. In the JSON example,
instances of ``JsonModule`` combines the functionality of standard modules
(``ModuleType``) and dictionaries::

    class JsonModule(ModuleType, dict):

        def __init__(self, specname):
            ModuleType.__init__(self, specname)
            dict.__init__(self)


``create_module`` instances and initializes the module::

    def create_module(self, spec)
        module = JsonModule(spec.name)
        self.init_module_attrs(spec, module)
        return module

Implementing ``execute_module``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``execute_module`` function should contain the code for loading the contents
of the module::

    def execute_module(self, module):
        module.clear()
        module.update(json.load(open(self.file_path)))
        return module

A good tip for determining how to implement this method is imagining you
trigger a reload of the module: the code syncing the module contents with the
file is what you should put here.

How does it work
----------------

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