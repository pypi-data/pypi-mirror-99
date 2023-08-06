import sys
if sys.version_info < (3, 6):
    raise ImportError('Python v3.6+ required; v%d.%d detected' % sys.version_info[:2])
del sys

from .core import (mod_tower,)

__all__ = [
    'mod_tower'
]