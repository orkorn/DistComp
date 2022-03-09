from setuptools import setup

setup(
    name='distcomp',
    version='0.1.0',
    description=("a tool for comparing distributions"),
    url='https://gh.internal.shutterfly.com/or-koren/distcomp',
    author='OR KOREN',
    author_email='or.koren@shutterfly.com',
    py_modules=['distcomp'],
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

