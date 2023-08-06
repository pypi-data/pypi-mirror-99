from setuptools import setup, find_packages
from io import open
from os import path

from more_kivy_app import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

URL = 'https://github.com/matham/more-kivy-app'

setup(
    name='more_kivy_app',
    version=__version__,
    author='Matthew Einhorn',
    author_email='moiein2000@gmail.com',
    license='MIT',
    description=(
        'Base class for kivy apps that is crash resistant with builtin '
        'configuration.'),
    long_description=long_description,
    url=URL,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    project_urls={
        'Bug Reports': URL + '/issues',
        'Source': URL,
    },
)
