from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Feature API utils'
LONG_DESCRIPTION = 'A package that allows to extract feature or data through API'

# Setting up
setup(
    name="phq_feature_api",
    version=VERSION,
    author="Tony Trinh",
    author_email="<tonytrinh0111@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['datetime', 'requests'],
    keywords=['python', 'events', 'feature'],
    classifiers=[
        "Development Status :: 1 - in progress",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
