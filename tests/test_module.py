import os
from anymod import ModuleLoader
from tests.modules.base.example_base import ExampleBase

config_path = os.path.dirname(os.path.realpath(__file__))
toml_path = config_path + '/settings.toml'

print(config_path)
print('relative', os.path.relpath(__file__, '.'))

mod = ModuleLoader(['tests/modules'])


def test_module_discovery():
    '''Dynamically load the appropriate module.'''
    assert mod.list_modules() == [
        'tests.modules.module',
        'tests.modules.module_class',
    ]
    module_path = mod.discover_module_path('module')
    assert module_path == 'tests.modules.module'


def test_class_load():
    module_path = mod.discover_module_path('module_class')
    assert module_path == 'tests.modules.module_class'

    module = mod.retrieve_subclass(module_path, ExampleBase)
    example_class = mod.load_classpath(module.__module__ + '.' + module.__name__)
    example = example_class()
    key = example.method1()
    assert key == 'value'
