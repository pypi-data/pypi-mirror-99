from setuptools import find_packages
from setuptools import setup
from os.path import splitext
from os.path import basename
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="datamx",
    version="0.9.1",
    package_dir={"": "src"},
    # packages=[""],
    packages=find_packages("src"),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],

    url="https://bitbucket.org/clockworkcodeteam/datamx/src/master/",
    license="GNU General Public License V3 or later",
    author="dilbertau99",
    author_email="dilbertau99@gmail.com",
    description="data structure for measurements/readings that can hold documentation about them and be read and written to/from objects to json and back",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="solar monitoring data format model",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: Communications",
    ],
    install_requires=["marshmallow", "marshmallow-oneofschema"],
)
