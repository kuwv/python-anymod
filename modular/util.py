# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control management of modules dynamically.'''

import importlib
import logging
import os
import sys
from typing import Any

log = logging.getLogger(__name__)


def add_module_path(path: str) -> None:
    '''Add module path to Python distribution.

    Parameters
    ----------
    path: str
        Path to add to Python distribution.

    '''
    if os.path.exists(path):
        if os.path.isfile(path):
            path = os.path.dirname(path)
        sys.path.append(path)
    else:
        print('path does not exist')


def remove_module_path(path: str) -> None:
    '''Remove module path from Python distribution.

    Parameters
    ----------
    path: str
        Path to remove from Python distribution.

    '''
    if path in sys.path:
        if os.path.isfile(path):
            path = os.path.dirname(path)
        sys.path.remove(path)
    else:
        print('path not loads')


def reload_module(module: Any) -> Any:
    '''Reload imported module.

    Parameters
    ----------
    module: Any
        Module to reload changes.

    '''
    try:
        module = importlib.reload(module)
    except ImportError:
        log.error("Failed to reload {}".format(module))
    return module
