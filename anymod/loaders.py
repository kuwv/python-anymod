# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control management of modules dynamically.'''

import importlib
import inspect
import logging
import os
import pkgutil
import sys

# from importlib.machinery import FileFinder
from types import ModuleType
from typing import Any, Dict, List, Optional

import pkg_resources

from . import util

log = logging.getLogger(__name__)


class PluginLoader:
    '''Load plugin modules dynamically.

    Overall tasks
    - Find packages / modules
    - Load packages / modules
    - Import objects

    '''

    # __module_path = None
    # __loader = None

    def __init__(
        self, paths: list = [], module_prefix: str = '', **kwargs: str,
    ):
        '''Initialize module loader plugin system.

        Parameters
        ----------
        paths: list
            Paths that can be searched for modules.
        prefix: str
            Module prefix to prepend to imported modules.

        '''

        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))
        if 'log_handler' in kwargs:
            log_handler = kwargs.pop('log_handler')
            log.addHandler(logging.StreamHandler(log_handler))  # type: ignore

        self.__paths = paths
        self.__module_prefix = module_prefix
        if self.__paths != []:
            for p in self.__paths:
                if p not in sys.path:
                    util.add_module_path(p)

    def find_packages(
        self,
        paths: List[str] = [],
        prefix: str = '',
        prefix_include: str = '',
        # prefix_exclude: str = '',
    ) -> List[Dict[str, Any]]:
        '''Retrieve list of modules matching prefix.

        Parameters
        ----------
        paths: list
            Paths to narrow search for plugins/modules.
        prefix: str
            Prefix to prepend to module imports.
        prefix_include: str
            Module prefix used to limit scope of search for modules.

        '''
        paths = paths if paths != [] else self.__paths
        prefix = prefix or self.__module_prefix
        modules = [
            {'name': name, 'ispkg': ispkg, 'finder': finder}
            for finder, name, ispkg in pkgutil.iter_modules(
                path=paths, prefix=prefix
            )
            if name.startswith(prefix_include)
        ]
        return modules

    def load_modules(
        self,
        paths: List[str] = [],
        prefix: str = '',
        prefix_include: str = '',
        # prefix_exclude: str = '',
    ) -> List[ModuleType]:
        '''Load list of modules matching prefix.

        Parameters
        ----------
        prefix_include: str
            Module prefix used to limit scope of search for modules.

        '''
        return [
            importlib.import_module(x['name'])
            for x in self.find_packages(
                paths=paths, prefix=prefix, prefix_include=prefix_include
            )
        ]

    def list_modules(self, paths: List[str] = [], **kwargs: str) -> List[Any]:
        '''Retrieve list of modules from specified path with matching prefix.

        Parameters
        ----------
        paths: list
            List of paths to search for modules.

        '''
        modules = []
        for x in self.find_packages(paths=paths, **kwargs):
            if x['ispkg'] is False and not x['name'].startswith('_'):
                modules.append(
                    f"{os.path.join(x['finder'].path, x['name'])}.py"
                )
            else:
                modules += self.list_modules(
                    paths=[os.path.join(x['finder'].path, x['name'])], **kwargs,
                )
        return modules

    def list_imports(
        self,
        base_path: Optional[str] = None,
        paths: List[str] = [],
        **kwargs: str,
    ) -> List[Any]:
        '''Retrieve list of modules from specified path with matching prefix.

        Parameters
        ----------
        paths: list
            List of paths to search for modules.

        '''
        modules = []
        for x in self.find_packages(paths=paths, **kwargs):
            # Determine module path
            if base_path:
                import_path = f"{base_path}.{x['name']}"
            else:
                import_path = x['name']

            # Populate module list
            if x['ispkg'] is False and not x['name'].startswith('_'):
                modules.append(import_path)
            else:
                modules += self.list_imports(
                    base_path=import_path,
                    paths=[os.path.join(x['finder'].path, x['name'])],
                    **kwargs,
                )
        return modules

    def get_import_path(
        self, name: str, path: str, **kwargs: str,
    ) -> Optional[str]:
        '''Retrieve module path with matching prefix.

        Parameters
        ----------
        name: str
            Name of the module.
        paths: str
            Path to search for module.

        '''
        # TODO: add try / catch
        result = next(
            (
                x
                for x in self.list_imports(paths=[path], **kwargs)
                if name == x.split('.')[-1]
                # if name == x.split(os.sep)[-1].split('.')[0]
            ),
            None,
        )
        return result

    @staticmethod
    def discover_entry_points(
        group: str, name: Optional[str] = None,
    ) -> Dict[str, Any]:
        '''Retrieve entry points of module.

        Parameters
        ----------
        group: str
            Group of entry points to retrieve.
        name: str
            Name of entry point within a group to retrieve.

        '''
        return {
            x.name: x.load()
            for x in pkg_resources.iter_entry_points(group, name)
        }

    @staticmethod
    def retrieve_subclass(module_path: str, subclass: Any) -> Optional[str]:
        '''Retrieve subclass inherrited from abstract.

        Parameters
        ----------
        module_path: str
            Name of the module to query for class objects.
        subclass: Any
            Subclass to query child types.

        '''
        # TODO: need to fix import_module check
        # if module_path not in sys.modules:
        module_import = importlib.import_module(module_path, package=__name__)
        for attribute_name in dir(module_import):
            attribute = getattr(module_import, attribute_name)
            if inspect.isclass(attribute) and issubclass(attribute, subclass):
                if subclass.__name__ != attribute.__name__:
                    setattr(sys.modules[__name__], module_path, attribute)
                    return attribute
        else:
            return None

    @staticmethod
    def load_classpath(classpath: str, package: Optional[str] = None) -> str:
        '''Load class from module.

        Parameters
        ----------
        classpath: str
            Python import path for class to be loaded.
        package: str, optional
            Package container classpath to be loaded.

        '''
        logging.info("Loading class {}".format(classpath))
        try:
            module_path, class_name = classpath.rsplit('.', 1)
            # TODO: need to fix import_module check
            # if module_path not in sys.modules:
            module = importlib.import_module(module_path, package=package)
        except ImportError:
            logging.error("Failed to load {}".format(class_name))
        return getattr(module, class_name)
