# type: ignore

import inspect
# import importlib
import os
import pkgutil
import sys

import pkg_resources

from anymod import PluginLoader  # , util

# config_path = os.path.dirname(os.path.realpath(__file__))
# toml_path = os.path.join(config_path, 'settings.toml')
print(sys.path)
mock_path = os.path.join(
    os.path.dirname(__file__),
    # 'tests',
    'mock_module',
    'mock_module',
)
loader = PluginLoader([mock_path])


def test_paths():
    assert mock_path in sys.path
    print([x for x in pkgutil.iter_modules([mock_path])])


def test_entry_point(setup_mock_modules):
    '''Dynamically load entry point modules.'''
    EntryTest = pkg_resources.load_entry_point(
        'mock_module', 'mock_module.modules', 'modules'
    )
    assert inspect.isclass(EntryTest) is True
    entry_test = EntryTest()
    assert entry_test.key == 'value'


def test_discover_plugins(setup_mock_modules):
    # mock_module = importlib.import_module('mock_module')
    # util.reload_module(mock_module)
    plugins = loader.discover_plugins(prefix_include='mock')
    print(type(plugins))


def test_discover_entry_points(setup_mock_modules):
    EntryTest = loader.discover_entry_points('mock_module.modules')['modules']
    assert inspect.isclass(EntryTest) is True
    entry_test = EntryTest()
    assert entry_test.key == 'value'


# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
# def test_spec_load(setup_mock_modules):
#     abs_mock_path = os.path.join(
#         os.path.dirname(__file__), 'mock_module', 'mock_module', '__init__.py'
#     )
#     spec = importlib.util.spec_from_file_location(
#         "mock_module.module", abs_mock_path
#     )
#     print(spec.__dict__)
#     module = importlib.util.module_from_spec(spec)
#     sys.modules[spec.name] = module
#     spec.loader.exec_module(module)
#     # mock_module.EntryTest()
#     print(type(module))
#     # print(mock_module.__dict__)


def test_discover_module_path():
    '''Dynamically load the appropriate module.'''
    # print(sys.meta_path)
    module = [
        {'finder': finder, 'name': name, 'ispkg': ispkg}
        for finder, name, ispkg in pkgutil.iter_modules(
            [mock_path], prefix='mock'
        )
    ]
    sys.path.append(module[0]['finder'].path)
    from mock_module.module import EntryTest

    assert inspect.isclass(EntryTest) is True
    entry_test = EntryTest()
    assert entry_test.key == 'value'


def test_dynamic_list_local_module():
    # assert loader.list_modules() == [
    #     'mock_module.example_base',
    #     'mock_module.module',
    #     'mock_module.module_class',
    # ]
    # module_path = loader.discover_module_path('module')
    # print(module_path)
    # assert module_path == 'mock_module.module'

    # EntryTest = loader.load_classpath(
    #     "{m}.{c}".format(m=module_path, c='EntryTest')
    # )

    module = loader.discover_modules(
        prefix='p_',
        prefix_include='',
        # prefix_exclude='p_',
    )

    print(module)
    if module != []:
        sys.path.append(module[0]['finder'].path)


def test_class_load(setup_mock_modules):
    '''Test loading classes.'''
    pass
    # from mock_module.example_base import ExampleBase
    # assert 'mock_module.example_base' in sys.modules

    # module_path = loader.discover_module_path('module_class')
    # assert module_path == 'mock_module.module_class'

    # module = loader.retrieve_subclass(module_path, ExampleBase)
    # example_class = loader.load_classpath(
    #     "{m}.{n}".format(m=module.__module__, n=module.__name__)
    # )
    # example = example_class()
    # key = example.method1()
    # assert key == 'value'
