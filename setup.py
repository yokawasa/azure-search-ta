import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('lib/azuresearchta.py', 'r') as fd:
    version = re.search(
        r'^_AZURE_SEARCH_TEXT_ANALYZE_VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(), re.MULTILINE).group(1)

setup(name='azure-search-ta',
    version=version,
    description='Azure Search Text Analyze command line tool',
    author='Yoichi Kawasaki',
    author_email='yoichi.kawasaki@outlook.com',
    url='https://github.com/yokawasa/azure-search-ta',
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
        'BeautifulSoup'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    keywords='azure search azuresearch text analysis api',
)
