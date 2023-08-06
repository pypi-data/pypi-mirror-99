from setuptools import setup, find_packages
from os import path

VERSION = '1.0.0'

# read the contents of the README file
this_directory = path.abspath( path.dirname ( __file__ ) )
with open( path.join( this_directory, 'README.md' ), encoding='utf-8' ) as f:
    long_description = f.read()


setup(
    name = "youtube_synopsis",
    version = VERSION,
    author = 'Tony Feng',
    description = 'Generate a colored, striped "summary" of a Youtube video.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://pypi.org/project/youtube-synopsis/',
    
    packages = find_packages(),
    install_requires = [
    'certifi==2020.12.5',
    'h11==0.12.0',
    'httpcore==0.12.3',
    'httpx==0.17.1',
    'idna==3.1',
    'joblib==1.0.1',
    'numpy==1.20.1',
    'opencv-python==4.5.1.48',
    'progress==1.5',
    'rfc3986==1.4.0',
    'scikit-learn==0.24.1',
    'scipy==1.6.1',
    'sniffio==1.2.0',
    'threadpoolctl==2.1.0',
    'youtube-dl==2021.3.14',
    'youtube-search-python==1.4.2' ]
 )