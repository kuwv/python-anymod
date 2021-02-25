# type: ignore
'''Provide pytest fixture for flask.'''

import os
import sys
import subprocess

import pytest


@pytest.fixture(autouse=True)
def setup_mock_modules():
    '''Add / remove module to test path.'''
    mock_module = os.path.join(
        os.path.dirname(__file__), 'mock_module-0.0.1-py3-none-any.whl'
    )
    subprocess.call([
        sys.executable,
        '-m',
        'pip',
        '--disable-pip-version-check',
        'install',
        mock_module,
    ])
    yield
    subprocess.call([
        sys.executable,
        '-m',
        'pip',
        '--disable-pip-version-check',
        'uninstall',
        'mock-module',
        '-y',
    ])
    for k in list(sys.modules.keys()):
        if k.startswith('mock_module'):
            del(sys.modules[k])
