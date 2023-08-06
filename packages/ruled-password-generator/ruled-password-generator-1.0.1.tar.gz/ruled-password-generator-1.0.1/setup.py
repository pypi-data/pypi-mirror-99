import io
import os
import sys

from setuptools import setup

# Package meta-data.
NAME = 'ruled-password-generator'
DESCRIPTION = 'Password generator with customizable rules.'
URL = 'https://github.com/hkcomori/ruled-password-generator'
EMAIL = 'hkcomori@gmail.com'
AUTHOR = 'hkcomori'
LICENSE = 'MIT'

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

required = []

setup(
    name=NAME,
    version=os.environ.get('PACKAGE_VERSION', '0.0.0'),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    py_modules=['ruled_password_generator'],
    install_requires=required,
    python_requires='>=3.7',
    extras_require={
        'cpu': [],
        'gpu': [],
    },
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)