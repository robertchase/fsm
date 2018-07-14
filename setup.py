from setuptools import find_packages
from distutils.core import setup

setup(
    name='fsm',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    description='A finite state machine library',
    long_description="""
Documentation
-------------
    You can see the project and documentation at the `GitHub repo <https://github.com/robertchase/fsm>`_
    """,
    author='Bob Chase',
    url='https://github.com/robertchase/fsm',
    license='MIT',
)
