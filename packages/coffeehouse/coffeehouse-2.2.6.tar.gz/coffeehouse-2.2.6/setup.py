from setuptools import setup
#from coffeehouse import __version__, __author__
# This causes an issue during the installation process

with open('README.md') as file:
    long_description = file.read()

setup(
    name='coffeehouse',
    version='2.2.6',
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
    author='Intellivoid Technologies',
    author_email='netkas@intellivoid.net',
    url='https://coffeehouse.intellivoid.net/',
    install_requires=[
        'requests>=2.3.0',
    ],
)
