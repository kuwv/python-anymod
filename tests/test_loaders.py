# type: ignore
'''Provide tests for loaders.'''

import inspect
import os
import sys

import pkg_resources

from anymod import PluginLoader

# config_path = os.path.dirname(os.path.realpath(__file__))
# toml_path = os.path.join(config_path, 'settings.toml')
mock_path = os.path.join(os.path.dirname(__file__), 'mock_module')
loader = PluginLoader([mock_path])


def test_paths():
    assert mock_path in sys.path
    mock_module = loader.find_packages(name='mock_module')[0]
    assert mock_module['name'] == 'mock_module'
    assert mock_module['module_finder'].path == mock_path


def test_entry_point(setup_mock_modules):
    '''Dynamically load entry point modules.'''
    EntryTest = pkg_resources.load_entry_point(
        'mock_module', 'mock_module.modules', 'modules'
    )
    assert inspect.isclass(EntryTest) is True
    entry_test = EntryTest()
    assert entry_test.key == 'value'


def test_load_modules(setup_mock_modules):
    # mock_module = importlib.import_module('mock_module')
    # util.reload_module(mock_module)
    plugins = loader.load_modules(prefix_include='mock')
    print(type(plugins))


def test_discover_entry_points(setup_mock_modules):
    EntryTest = loader.discover_entry_points('mock_module.modules')['modules']
    assert inspect.isclass(EntryTest) is True
    entry_test = EntryTest()
    assert entry_test.key == 'value'


# https://stackoverflow.com/questions/67631
# def test_spec_load(setup_mock_modules):
#     spec = importlib.util.spec_from_file_location(
#         "mock_module.module", mock_path
#     )
#     print(spec.__dict__)
#
#     module = importlib.util.module_from_spec(spec)
#     sys.modules[spec.name] = module
#     spec.loader.exec_module(module)
#
#     # mock_module.EntryTest()
#     print(type(module))
#     # print(mock_module.__dict__)


def test_dynamic_list_local_module():
    assert loader.list_imports() == [
        'mock_module.example_base',
        'mock_module.module',
        'mock_module.module_class',
        'mock_module.nested1.module1',
        'mock_module.nested1.nested2.module2',
    ]
    module_path = loader.get_import_path('module', mock_path)
    assert module_path == 'mock_module.module'

    EntryTest = loader.load_classpath(
        "{m}.{c}".format(m=module_path, c='EntryTest')
    )

    module = loader.find_packages()
    #     prefix='p_',
    #     prefix_include='',
    #     # prefix_exclude='p_',
    # )

    # print(module)
    # if module != []:
    #     sys.path.append(module[0]['module_finder'].path)

    sys.path.append(module[0]['module_finder'].path)
    from mock_module.module import EntryTest

    assert inspect.isclass(EntryTest) is True
    entry_test = EntryTest()
    assert entry_test.key == 'value'


def test_class_load(setup_mock_modules):
    '''Test loading classes.'''
    from mock_module.example_base import ExampleBase

    assert 'mock_module.example_base' in sys.modules

    module_path = loader.get_import_path('module_class', mock_path)
    assert module_path == 'mock_module.module_class'

    module = loader.retrieve_subclass(module_path, ExampleBase)
    example_class = loader.load_classpath(
        "{m}.{n}".format(m=module.__module__, n=module.__name__)
    )
    example = example_class()
    key = example.method1()
    assert key == 'value'
