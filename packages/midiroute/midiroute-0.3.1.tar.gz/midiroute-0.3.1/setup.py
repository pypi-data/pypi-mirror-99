"""A command line utility for routing and monitoring MIDI ports."""

import pathlib

from setuptools import find_packages, setup

root_dir = pathlib.Path(__file__).absolute().parent

# Get the long description from the README file
with open(str(pathlib.Path(root_dir, "README.md")), encoding="utf-8") as f:
    long_description = f.read()

DESCRIPTION = __doc__
INSTALL_REQUIRES = ["click", "mido", "python-rtmidi", "tabulate"]

setup(
    name="midiroute",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atticave/midiroute",
    author="atticave",
    author_email="atticave@blueheaps.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="midi interface router monitor diagnostics",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["midiroute=midiroute.main:main"]},
)
