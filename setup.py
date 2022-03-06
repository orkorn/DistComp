from setuptools import setup

from comparing_distributions import __version__

setup(
    name='distcomp',
    version='0.1.0',
    description=("a tool for comparing disterbutions"),
    url='https://gh.internal.shutterfly.com/or-koren/distcomp',
    author='OR KOREN',
    author_email='or.koren@shutterfly.com',
    py_modules=['DistComp'],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'scipy',
        'seaborn',
        'matplotlib',
        'termcolor',
        'causalml']

    )

