'''Simple module loading tool.'''
# -*- coding: utf-8 -*-

__author__ = 'Jesse P. Johnson'
__title__ = 'anymod'
__version__ = '0.1.1-dev4'
__license__ = 'Apache-2.0'

__all__ = ['ModuleLoader']

import logging

from .module import ModuleLoader  # noqa

logging.getLogger(__name__).addHandler(logging.NullHandler())
