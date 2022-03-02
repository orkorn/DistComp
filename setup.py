from setuptools import setup

from my_pip_package import __version__

setup(
    name='comparing_distributions',
    version=__version__,
    url='https://gh.internal.shutterfly.com/or-koren/distribution-comparison',
    author='OR KOREN',
    author_email='or.koren@shutterfly.com',
    py_modules=['comparing_distributions'],
)
