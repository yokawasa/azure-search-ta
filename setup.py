#!/usr/bin/env python
import re
import ast

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

with open('lib/azuresearchta.py', 'r') as fd:
    version = re.search(
        r'^_AZURE_SEARCH_TEXT_ANALYZE_VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(), re.MULTILINE).group(1)

setup(name='azure-search-ta',
    version=version,
    description='Azure Search Test Analyzer API Client Tool',
    long_description=long_description,
    author='Yoichi Kawasaki',
    author_email='yoichi.kawasaki@outlook.com',
    url='https://github.com/yokawasa/azure-search-ta',
    download_url='https://pypi.python.org/pypi/azure-seatch-ta',
    platforms='any',
    license='MIT',
    package_dir = {'': 'lib'},
    py_modules=['azuresearchta'],
    entry_points={
        'console_scripts': 'azure-search-ta=azuresearchta:main',
    },
    install_requires=[
        'argparse',
        'simplejson',
        'beautifulsoup4'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords='azure search azuresearch text analysis api',
)
