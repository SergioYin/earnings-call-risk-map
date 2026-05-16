"""Public API for earnings-call-risk-map."""

from .core import analyze_document, compare_snapshots
from .version import __version__

__all__ = ["__version__", "analyze_document", "compare_snapshots"]
