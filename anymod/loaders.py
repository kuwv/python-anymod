# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control management of modules dynamically.'''

import importlib
import inspect
import logging
# import os
import pkgutil
import sys
from importlib.machinery import FileFinder
from types import ModuleType
from typing import Any, Dict, List, Optional, Union

import pkg_resources

from . import util

log = logging.getLogger(__name__)


class PluginLoader:
    '''Load plugin modules dynamically.'''

    __module_path = None
    # __loader = None

    def __init__(
        self,
        paths: list = [],
        module_prefix: str = '',
        **kwargs: str,
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

    @staticmethod
    def discover_plugins(
        paths: Union[List[str], str] = [],
        prefix: str = '',
        prefix_include: str = '',
        # prefix_exclude: str = '',
    ) -> List[ModuleType]:
        '''Retrieve list of modules matching prefix.

        Parameters
        ----------
        prefix_include: str
            Module prefix used to limit scope of search for modules.

        '''
        return [
            importlib.import_module(name)
            for finder, name, ispkg in pkgutil.iter_modules(
                path=paths, prefix=prefix
            )
            if name.startswith(prefix_include)
        ]

    def discover_modules(
        self,
        paths: List[str] = [],
        prefix: str = '',
        prefix_include: str = '',
        # prefix_exclude: str = '',
    ) -> List[Dict[str, Union[str, FileFinder, bool]]]:
        '''Retrieve list of modules matching prefix.

        Parameters
        ----------
        prefix: str
            Prefix to prepend to module imports.
        prefix_include: str
            Module prefix used to limit scope of search for modules.

        '''
        paths = paths if paths != [] else self.__paths
        prefix = prefix or self.__module_prefix
        module = [
            {'name': name, 'ispkg': ispkg, 'finder': finder}
            for finder, name, ispkg in pkgutil.iter_modules(
                path=paths, prefix=prefix
            )
            if name.startswith(prefix_include)
        ]
        return module

    @staticmethod
    def discover_entry_points(
        group: str,
        name: Optional[str] = None,
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
    def retrieve_subclass(
        module_name: str,
        subclass: Any,
    ) -> Optional[str]:
        '''Retrieve subclass from module

        Parameters
        ----------
        module_name: str
            Name of the module to query for class objects.
        subclass: Any
            Subclass to query child types.

        '''
        module_import = importlib.import_module(module_name, __name__)
        for attribute_name in dir(module_import):
            attribute = getattr(module_import, attribute_name)
            if inspect.isclass(attribute) and issubclass(attribute, subclass):
                if subclass.__name__ != attribute.__name__:
                    setattr(sys.modules[__name__], module_name, attribute)
                    return attribute
        else:
            return None

    @staticmethod
    def load_classpath(
        classpath: str,
        package: Optional[str] = None
    ) -> str:
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
            module = importlib.import_module(module_path, package)
        except ImportError:
            logging.error("Failed to load {}".format(class_name))
        return getattr(module, class_name)

    def _get_import_path(
        self,
        name: str,
        path: str,
        module: Optional[str] = None,
        subclass: Optional[str] = None,
    ) -> str:
        '''Module paths.

        Parameters
        ----------
        name: str
            Module name
        path: str
            Path to module
        module: str, optional
            Is this the same as the name of the module?
        subclass: str, optional
            Mixin / Baseclass that is inherrited

        '''
        # TODO: Add exclusions, os.path.relpath
        module_path = "{p}.{n}".format(p=path, n=name)
        if module is not None and subclass is not None:
            module_path = self.retrieve_subclass(
                module, subclass
            )  # type: ignore
        return module_path

    def list_modules(
        self,
        prefix: str = '',
        paths: List[str] = [],
        **kwargs: str,
    ) -> List:
        '''Retrieve list of modules from specified path with matching prefix.

        Parameters
        ----------
        paths: list
            List of paths to search for modules.

        '''
        paths = paths if paths != [] else self.__paths
        prefix = prefix if prefix != '' else self.__module_prefix
        result = [
            self._get_import_path(name, finder.path, **kwargs)
            for finder, name, _ in pkgutil.iter_modules(
                path=paths, prefix=prefix
            )
        ]
        return result

    def discover_module_path(
        self,
        name: str,
        prefix: Optional[str] = None,
        paths: List[str] = [],
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
                for x in self.list_modules(prefix, paths)
                if name == x.split('.')[-1]
            ),
            None,
        )
        return result
