#!/usr/bin/env python
#
# This is a wrapper module for different platform implementations
#
# This file is part of runer. https://github.com/
# (C) 2001-2021 Pytool Li <pytli@celestica.com>
#
# SPDX-License-Identifier:    BSD-3-Clause

from __future__ import absolute_import

import sys
import importlib
from .modules import register,AutoLoadModules
from .runer import run,u,b
__all__ = ["register","run","put"]

__version__ = '3.5'

VERSION = __version__

AutoLoadModules()

# pylint: disable=wrong-import-position
if sys.platform == 'cli':
    pass
else:
    import os
    # chose an implementation, depending on os
    if os.name == 'nt':  # sys.platform == 'win32':
        pass
    elif os.name == 'posix':
        pass  # noqa
    elif os.name == 'java':
        pass
    else:
        raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
