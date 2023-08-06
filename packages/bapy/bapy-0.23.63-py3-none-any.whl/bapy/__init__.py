#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""Bapy Package."""
import typer

from .core import *
from .echo import *
# from .ipfull import *
# from .libfull import *
# from .mongofull import *
# __version__ = core.__version__

__all__ = core.__all__ + echo.__all__
# __all__ = core.__all__ + ipfull.__all__ + libfull.__all__ + mongofull.__all__

if __name__ == '__main__':
    try:
        typer.Exit(app())
    except KeyboardInterrupt:
        red('Aborted!')
        typer.Exit()
