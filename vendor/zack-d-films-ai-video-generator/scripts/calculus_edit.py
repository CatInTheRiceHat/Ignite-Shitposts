#!/usr/bin/env python3
"""Compatibility facade; execute canonical source so imports expose the real API."""
import sys
from pathlib import Path
_workflow = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_workflow / 'scripts'))
_source = _workflow / "scripts/calculus_edit.py"
__file__ = str(_source)
exec(compile(_source.read_text(), str(_source), 'exec'), globals())
