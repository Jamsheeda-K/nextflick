from setuptools import setup, find_packages
import os

def open_file(fname):
    """helper function to open a local file"""
    return open(os.path.join(os.path.dirname(__file__), fname))

setup(
    name='nextflick',
    version='0.0.1',
    author='Jamsheedak@gmail.com',
    author_email='jamsheedak@gmail.com',
    packages=find_packages(),
    url='https://github.com/jamsheeda-K/',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    description='NextFlick is a Python library for movie recommendations',
    long_description=open_file('README.md').read(),
    # end user dependencies for your library
    install_requires=['pandas','scikit-learn','fuzzywuzzy','python-Levenshtein' ],
    # include additional data
    package_data= {
         'nextflick': ['data/*.csv','data/*.pickle']
     }
)
