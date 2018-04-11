import os
import sys
from setuptools import setup, find_packages
sys.path.append('expstock')

__version__ = '0.1.0'
__author__ = 'Chie Hayashida'
__author_email__ = 'chie-hayashida@cookpad.com'
__classifiers__ = (
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: User Interfaces')

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    readme = f.read()

with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open('test_requirements.txt') as f:
    tests_require= f.read().splitlines()

setup(
    name='expstock',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/chie8842/expstock',
    description='Stock your experiments',
    scripts=['scripts/expstock-server'],
    data_files=[('expstock/template', ['expstock/template/index.html'])],
    long_description=readme,
    test_suite='test',
    tests_require=tests_require,
    classifiers=__classifiers__,
    packages=find_packages(),
    install_requires=requires,
    license='MIT')

