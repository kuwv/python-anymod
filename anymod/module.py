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
from typing import Any, Dict, List, Optional

import pkg_resources

# Current OS Platform filetypes
# FILETYPES = [
#     ('Source:', importlib.machinery.SOURCE_SUFFIXES),
#     ('Debug:', importlib.machinery.DEBUG_BYTECODE_SUFFIXES),
#     ('Optimized:', importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES),
#     ('Bytecode:', importlib.machinery.BYTECODE_SUFFIXES),
#     ('Extension:', importlib.machinery.EXTENSION_SUFFIXES),
# ]

log = logging.getLogger(__name__)


class ModuleLoader:
    '''Load modules dynamically.'''

    __module_path = None
    # __loader = None

    def __init__(
        self,
        path: Optional[list] = None,
        prefix: str = '',
        **kwargs: str
    ):
        '''Initialize module search paths.'''

        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))
        if 'log_handler' in kwargs:
            log_handler = kwargs.pop('log_handler')
            log.addHandler(logging.StreamHandler(log_handler))  # type: ignore

        self.__path = path
        self.__prefix = prefix
        if self.__path:
            (self.add_module_path(p) for p in self.__path)

    @staticmethod
    def add_module_path(path: str) -> None:
        '''Add module path to Python.'''
        sys.path.append(os.path.dirname(path))

    @staticmethod
    def discover_plugins(module_prefix: str) -> Dict[str, Any]:
        '''Retrieve list of modules matching prefix.'''
        return {
            name: importlib.import_module(name)
            for finder, name, ispkg in pkgutil.iter_modules()
            if name.startswith(module_prefix)
        }

    @staticmethod
    def discover_entry_points(entry: str) -> Dict[str, Any]:
        '''Retrieve entry points of module.'''
        return {
            entry_point.name: entry_point.load()
            for entry_point in pkg_resources.iter_entry_points(entry)
        }

    def __mod_path(
        self,
        name: str,
        path: str,
        module: Optional[str] = None,
        subclass: Optional[str] = None,
    ) -> str:
        '''Module paths.'''
        # TODO: Add exclusions, os.path.relpath
        module_path = "{p}.{n}".format(p=path.replace('/', '.'), n=name)
        if module is not None and subclass is not None:
            module_path = self.retrieve_subclass(
                module, subclass
            )  # type: ignore
        return module_path

    def list_modules(self, **kwargs: str) -> List:
        '''Retrieve list of modules from specified path with matching prefix.'''
        result = [
            self.__mod_path(name, finder.path, **kwargs)
            for finder, name, _ in pkgutil.iter_modules(
                path=self.__path, prefix=self.__prefix
            )
        ]
        return result

    def discover_module_path(self, module_name: str) -> List[str]:
        '''Retrieve module path with matching prefix.'''
        # TODO: add try / catch
        return next((x for x in self.list_modules() if (module_name in x)), [])

    def retrieve_subclass(
        self,
        module: str,
        subclass: Any,
    ) -> Optional[str]:
        '''Retrieve subclass from module'''
        module_import = importlib.import_module(module, __name__)
        for attribute_name in dir(module_import):
            attribute = getattr(module_import, attribute_name)
            if inspect.isclass(attribute) and issubclass(attribute, subclass):
                if subclass.__name__ != attribute.__name__:
                    setattr(sys.modules[__name__], module, attribute)
                    return attribute
        else:
            return None

    def reload_module(self, module: Any) -> Any:
        '''Reload imported module.'''
        try:
            module = importlib.reload(module)
        except ImportError:
            logging.error("Failed to reload {}".format(module))
        return module

    def load_classpath(
        self,
        classpath: str,
        package: Optional[str] = None
    ) -> str:
        '''Load class from module.'''
        logging.info("Loading class {}".format(classpath))
        try:
            module_path, class_name = classpath.rsplit('.', 1)
            module = importlib.import_module(module_path, package)
        except ImportError:
            logging.error("Failed to load {}".format(class_name))
        return getattr(module, class_name)
