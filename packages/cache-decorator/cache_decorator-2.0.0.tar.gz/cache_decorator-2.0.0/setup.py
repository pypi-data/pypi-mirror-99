import os
import re
# To use a consistent encoding
from codecs import open as copen

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with copen(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with copen(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("cache_decorator", "__version__.py")

test_deps =[
    "pytest",
    "pytest-cov",
    "coveralls",
    "validate_version_code",
    "codacy-coverage"
]

extras = {
    'test': test_deps,
    "numpy":["numpy", "dict_hash[numpy]"],
    "pandas":["pandas", "dict_hash[pandas]"],
    "excel":["openpyxl", "xlrd"],
    "numba":["dict_hash[numba]"],
}

extras["all"] = ["dict_hash[all]"] + [
    x
    for k, v in extras.items()
    for x in v
    if k != "test"
]

setup(
    name='cache_decorator',
    version=__version__,
    description="a simple decorator to cache the results of computationally heavy functions",
    long_description=long_description,
    url="https://github.com/zommiommy/cache_decorator",
    author="Tommaso Fontana",
    author_email="tommaso.fontana.96@gmail.com",
    # Choose your license
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    tests_require=test_deps,
    # Add here the package dependencies
    install_requires=[
        "dict_hash[compress_json] >= 1.1.16",  # This is used to get a consistent hash of the arguments
        "humanize",             # This is used for the metadata to be readable

        # The following packages have no dependancies so it should be safe to add
        "compress_pickle",      # For compressed pickles
        "compress_json",        # For compressed json
        "deflate_dict",         # To save arguments to the json
    ],
    extras_require=extras,
)
