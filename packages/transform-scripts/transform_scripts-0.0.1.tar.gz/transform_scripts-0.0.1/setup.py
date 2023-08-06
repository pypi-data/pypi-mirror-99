import re
from setuptools import find_packages, setup

# Read the version and package name from scripts/__init__.py
# From https://gehrcke.de/2014/02/distributing-a-python-command-line-application/
# Your setup.py should not import your package for reading the version number.
# Instead, always read it directly. In this case, I used regular expressions for extracting it.
version = re.search('^__version__\\s*=\\s*"(.*)"', open("transform_scripts/__init__.py").read(), re.M)
PACKAGE_NAME = re.search('^PACKAGE_NAME\\s*=\\s*"(.*)"', open("transform_scripts/__init__.py").read(), re.M)
if not version or not PACKAGE_NAME:
    raise Exception("Failed to parse transform_scripts/__init__.py for version and package name.")

setup(
    name=PACKAGE_NAME.group(1),
    version=version.group(1),
    # Note, we could possibly lower this but haven't yet tested older versions and haven't yet been asked to :)
    python_requires=">=3.6",
    author="Transform Data",
    author_email="bobby@transformdata.io",
    description=("Transform Scripts"),
    long_description="",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["tf = transform_scripts.validate"]},
    py_modules=["transform_scripts"],
    # Package details
    packages=find_packages(),
    include_package_data=True,
    # Dependencies
    setup_requires=["setupmeta"],
    install_requires=[
        "requests==2.23.0",
    ],
)
