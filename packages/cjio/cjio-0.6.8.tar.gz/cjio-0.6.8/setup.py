from setuptools import setup
from pathlib import Path
import cjio

CURRENT_DIR = Path(__file__).parent

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='cjio',
    version=cjio.__version__,
    description='CLI to process and manipulate CityJSON files',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/cityjson/cjio',
    author='Hugo Ledoux, Balázs Dukai',
    author_email='h.ledoux@tudelft.nl, b.dukai@tudelft.nl',
    python_requires='~=3.5',
    packages=['cjio'],
    package_data={'cjio': ['schemas/0.9/*', 'schemas/1.0.0/*', 'schemas/1.0.1/*']},
    # include_package_data=True,
    license = 'MIT',
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows'
    ],
    install_requires=[
        'Click',
        'jsonschema',
        'jsonref'
    ],
    entry_points='''
        [console_scripts]
        cjio=cjio.cjio:cli
    ''',
)
