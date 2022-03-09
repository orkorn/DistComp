import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='distcomp',
    version='0.1.0',
    author='OR-KOREN',
    author_email='orkorn@gmail.com',
    description='a tool for comparing distributions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/orkorn/distcomp',
    packages=['distcomp'],
    install_requires=['pandas',
        'numpy',
        'plotly',
        'scipy',
        'seaborn',
        'matplotlib',
        'termcolor',
        'causalml'],
)
