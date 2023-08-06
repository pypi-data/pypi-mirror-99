from setuptools import setup, find_packages
import os
import pathlib
VERSION = '0.0.4'
DESCRIPTION = 'Web Scraper to find and read your favourite Mangas'
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
# Setting up
setup(

    name="MangaScraper",
    version=VERSION,
    author="Tanmya Vishvakarma)",
    author_email="tanmya2000@gmail.com",
    license="MIT",
    description=DESCRIPTION,
    long_description=README,
    url="https://github.com/tanmyavishvakarma/MangaScraper",
    long_description_content_type="text/markdown",
    packages=['mangascraper'],
    install_requires=['bs4', 'requests'],
    keywords=['python', 'manga', 'scraper', 'mangascraper', 'anime', 'manga scraper'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
        entry_points={
        "console_scripts": [
            "mangascraper=mangascraper.__main__:main",
        ]
    }
)