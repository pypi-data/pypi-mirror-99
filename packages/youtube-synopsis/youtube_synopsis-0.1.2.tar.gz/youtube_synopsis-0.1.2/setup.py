from setuptools import setup, find_packages

VERSION = '0.1.2'

setup(
    name = "youtube_synopsis",
    version = VERSION,
    
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