# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
# type: ignore
'''Provide plugin base for test modules.'''
from abc import ABCMeta, abstractmethod


class ExampleBase(metaclass=ABCMeta):
    '''Define example test module methods.'''

    @abstractmethod
    def method1(self):
        '''Define example one test method.'''
