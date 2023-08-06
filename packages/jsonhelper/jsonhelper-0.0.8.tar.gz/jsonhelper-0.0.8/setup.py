#from distutils.core import setup
from setuptools import setup, find_packages
setup(
  name = 'jsonhelper',
  version = '0.0.8',
  description = 'JSON Tools',
  author = 'Alvaro De Leon',
  author_email = 'deleon@adl.com.uy',
  url = 'https://github.com/alvarodeleon/jsontools', # use the URL to the github repo
  download_url = 'https://github.com/alvarodeleon/jsontools/tarball/0.0.8',
  keywords = ['json'],
  classifiers = [],
  package_dir = {'':'src'},
  packages=find_packages(where='src')
)
