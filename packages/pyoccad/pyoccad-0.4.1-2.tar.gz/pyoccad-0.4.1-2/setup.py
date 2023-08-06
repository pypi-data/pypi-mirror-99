"""The Python setup script."""
from setuptools import setup

try:
    import OCC.Core
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        """
        ****
        Pyoccad requires package `pythonocc-core` 7.4.0, which is not available on PiPy.
        Please install pythonocc-core from conda or mamba:
        >>> conda install pythonocc-core -c conda-forge
        ****
        """
    )

setup()
