# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Simple plugin management tool.'''

import logging

from .loaders import PluginLoader  # noqa

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = 'Jesse P. Johnson'
__author_email__ = 'jpj6652@gmail.com'
__title__ = 'anymod'
__description__ = 'Inspection based parser built on argparse.'
__version__ = '0.1.1-dev10'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2020 Jesse Johnson.'
__all__ = ['PluginLoader', 'utils']
