# type: ignore
'''Example class to test loading.'''
from .base.example_base import ExampleBase


class ExampleClass(ExampleBase):
    '''Test class.'''

    def __init__(self):
        '''Initialize test.'''
        self.key = 'value'

    def method1(self):
        '''Implemented method1.'''
        return self.key
