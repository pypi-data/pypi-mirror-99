import os
import re
from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(
            1
        )


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="databases-extensions",
    version=get_version("extensions"),
    python_requires=">=3.6",
    url="https://github.com/chapagainmanoj/databases-query-extension",
    license="BSD",
    description="Extensions for sqlalchemy with databases",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Manoj Chapagain",
    author_email="chapagainmanoj35@gmail.com",
    packages=get_packages("extensions"),
    data_files=[("", ["LICENSE.md"])],
    install_requires=["databases", "pydantic"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)