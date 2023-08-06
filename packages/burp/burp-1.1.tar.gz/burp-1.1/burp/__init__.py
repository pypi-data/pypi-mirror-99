from __future__ import absolute_import

from .burpy import *
from .java_interfaces import *

install_java_interfaces()

import base64

__version__ = "1.1"
__author__ = "Erlend Leiknes"
__author_email__ = base64.b64decode("ZGV2QGxlaWtuLmVz")
__license__ = "MIT"
__url__ = "https://github.com/elnerd/burpy"

