# type: ignore
'''Provide pytest fixture for flask.'''

import os
import sys
import subprocess

import pytest


@pytest.fixture(autouse=True)
def setup_modules():
    '''Add / remove module to test path.'''
    mock_module = os.path.join(
        os.path.dirname(__file__), 'mock_module-0.0.1-py3-none-any.whl'
    )
    subprocess.check_call([
        sys.executable,
        '-m',
        'pip',
        '--disable-pip-version-check',
        'install',
        mock_module,
    ])
    yield
    subprocess.check_call([
        sys.executable,
        '-m',
        'pip',
        '--disable-pip-version-check',
        'uninstall',
        'mock-module',
        '-y',
    ])
    pass
