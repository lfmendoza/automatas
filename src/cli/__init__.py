"""
Command-line interface module.
"""

from .argument_parser import build_argument_parser
from .batch_processor import run_batch

__all__ = [
    "build_argument_parser",
    "run_batch",
] 