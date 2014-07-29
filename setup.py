import os

from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(name='pwt',
      version='0.1.0',
      description='Python package for working with Penn World Tables (PWT) data.',
      )
