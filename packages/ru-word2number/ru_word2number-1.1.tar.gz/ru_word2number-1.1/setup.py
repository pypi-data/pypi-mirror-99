import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
  name = 'ru_word2number',
  packages = ['ru_word2number'],  # this must be the same as the name above
  version = '1.1',
  license=open('LICENSE.txt').read(),
  description = 'Convert russian number words eg. триста сорок два to numbers (342).',
  author = 'Oknolaz',
  author_email = 'oknolaz.freedom@protonmail.com',
  url = 'https://github.com/Oknolaz/Russian_w2n',  # use the URL to the github repo
  download_url = 'https://github.com/Oknolaz/Russian_w2n/tarball/1.1', 
  keywords = ['numbers', 'convert', 'words'],  # arbitrary keywords
  classifiers = [
      'Intended Audience :: Developers',
      'Programming Language :: Python'
  ],
  long_description='Convert russian number words to numbers.'
)
