from . import api
from . import exception
from . import lydia
from . import nsfw_classification
from .api import *  # noqa: F403,F401
from .exception import *  # noqa: F403,F401
from .lydia import *  # noqa: F403,F401
from .nsfw_classification import *  # noqa: F403,F401

__all__ = (
    [
        'api',
        'exception',
        'lydia',
        'nsfw_classification',
    ]
    + api.__all__
    + exception.__all__
    + lydia.__all__
    + nsfw_classification.__all__
)

__version__ = '2.1.0'
__author__ = 'Intellivoid Technologies'
__source__ = 'https://github.com/intellivoid/CoffeeHouse-Python-API-Wrapper'
__copyright__ = 'Copyright (c) 2017-2021 ' + __author__
