"""A solution for chatbot constructors to identify problems in flow structure.

Main Features
-------------
  * Automated and fast flow structure analysis;
  * Implement most know flow structure analysis;
"""

from __future__ import annotations

__author__ = "Squad XD"
__version__ = "0.6.1"

from .core import Flow
from .abstract import Analyser
from .analysis import (
    DuplicatedPaths,
    LongScript,
    MissingTrackings,
    ProcessHTTPReturnValidation,
)
