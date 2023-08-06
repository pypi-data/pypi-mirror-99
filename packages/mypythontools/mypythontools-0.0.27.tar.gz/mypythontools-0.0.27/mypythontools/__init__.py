"""
mypythontools
=============

Some tools/functions/snippets used across projects.

Official documentation - https://mypythontools.readthedocs.io/
Official repo - https://github.com/Malachov/mypythontools

Usually used from IDE. Used paths are infered and things like building the
application with pyinstaller incrementing version, generating rst files for sphinx docs,
pushing to github or deploying to Pypi is matter of calling one function
or clicking one button (e.g. Vs code task).

Many projects - one codebase.

If you are not sure whether structure of app that will work with this code, there is python starter repo
on https://github.com/Malachov/my-python-starter

Paths are infered, but if you have atypical structure or have more projects in cwd, use `mypythontools.misc.set_paths()`.
"""

from . import utils
from . import build
from . import deploy
from . import misc
from . import pyvueeel

__version__ = "0.0.27"

__author__ = "Daniel Malachov"
__license__ = "MIT"
__email__ = "malachovd@seznam.cz"

__all__ = ['utils', 'build', 'deploy', 'misc', 'pyvueeel']
