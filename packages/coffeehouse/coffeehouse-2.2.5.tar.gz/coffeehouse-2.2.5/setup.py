from setuptools import setup
from coffeehouse import __version__, __author__

with open('README.md') as file:
    long_description = file.read()

setup(
    name='coffeehouse',
    version=__version__,
    description='Official CoffeeHouse API Wrapper for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'coffeehouse',
        'coffeehouse.lydia',
        'coffeehouse.nsfw_classification',
    ],
    package_dir={
        'coffeehouse': 'coffeehouse',
    },
    author=__author__,
    author_email='netkas@intellivoid.net',
    url='https://coffeehouse.intellivoid.net/',
    install_requires=[
        'requests>=2.3.0',
    ],
)
