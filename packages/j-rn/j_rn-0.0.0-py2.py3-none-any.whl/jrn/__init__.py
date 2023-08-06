"""
Utilities for The Journal of Reproducible Notebooks (J-RN).
"""
__author__ = "Casper da Costa-Luis"
__date__ = "2021"
# version detector. Precedence: installed dist, git, 'UNKNOWN'
try:
    from ._dist_ver import __version__
except ImportError: # pragma: nocover
    try:
        from setuptools_scm import get_version

        __version__ = get_version(root="..", relative_to=__file__)
    except (ImportError, LookupError):
        __version__ = "UNKNOWN"

from miutil.web import urlopen_cached


def download(url, outdir=".", fname=None):
    """
    Downloads <url> to <outdir> if not already present.

    Args:
      outdir (str or Path): output directory.
      url (str): remote address.
      fname (str): automatic if not specified.
    Returns:
      str: output filename.
    """
    out = urlopen_cached(url, outdir, fname=fname)
    out.close()
    return out.name
