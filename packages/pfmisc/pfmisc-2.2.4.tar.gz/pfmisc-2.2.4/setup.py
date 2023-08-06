import sys
# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'pfmisc',
      version          =   '2.2.4',
      description      =   'Misc utilities for FNNDSC python repos',
      long_description =   readme(),
      author           =   'Rudolph Pienaar',
      author_email     =   'rudolph.pienaar@gmail.com',
      url              =   'https://github.com/FNNDSC/pfmisc',
      packages         =   ['pfmisc'],
      install_requires =   ['pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['bin/pfmisc'],
      license          =   'MIT',
      zip_safe         =   False
     )
