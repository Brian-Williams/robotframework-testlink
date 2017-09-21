"""
Basic set of tests that apply to every python repo.

It's main purpose is to avoid pytest exit code 5 (no tests found) by providing some test to any repo without resorting
to a travis script that could potentially hide real problems:
- '[ "$(ls -A ./tests)" ] && pytest || echo "No tests in repo"'
"""
import importlib
from robottestlink import __title__


def test_import():
    importlib.import_module(__title__)
