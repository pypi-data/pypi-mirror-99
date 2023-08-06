from setuptools import setup
from setuptools import find_packages
import re
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))

with open(join(CURDIR, "src", "game_of_life", "__init__.py"), encoding="utf-8") as f:
    VERSION = re.search('\n__version__ = "(.*)"', f.read()).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="menkeyshow.conway",
    version=VERSION,
    author="Maximilian Birkenhagen",
    author_email="maximilian.birkenhagen@gmail.com",
    description="Python implementation of Conway's Game of Life",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Menkeyshow/game_of_life",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        'console_scripts': [
            'conway = game_of_life.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)