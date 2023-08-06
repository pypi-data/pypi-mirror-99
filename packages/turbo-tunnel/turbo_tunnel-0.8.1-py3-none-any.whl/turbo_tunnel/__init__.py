# -*- coding: utf-8 -*-

"""Turbo tunnel
"""

VERSION = "0.8.1"

import sys
import traceback

try:
    from . import https
    from . import server
    from . import socks

    if sys.version_info[1] >= 6:
        # ssh disabled in python 3.5
        from . import ssh
    from . import tunnel
    from . import websocket
except ImportError:
    traceback.print_exc()
