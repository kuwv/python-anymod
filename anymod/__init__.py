# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Simple module loading tool.'''

__author__ = 'Jesse P. Johnson'
__title__ = 'anymod'
__version__ = '0.1.1-dev7'
__license__ = 'Apache-2.0'

__all__ = ['ModuleLoader']

import logging

from .module import ModuleLoader  # noqa

logging.getLogger(__name__).addHandler(logging.NullHandler())
