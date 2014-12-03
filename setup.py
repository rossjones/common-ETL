from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='openaddresses',
    version='0.0.3',
    description='ETL scripts for OpenAddresses',
    url='https://github.com/OpenAddressesUK/common-ETL',
    author='John Murray',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'MySQL-python==1.2.5',
        'pyshp==1.2.1',
        'docopt==0.6.2',
        'requests==2.5.0'
    ],
    package_data={
        'sql': ['os_alpha_etl.sql'],
    },
    entry_points = {
        'console_scripts': ['etl=openaddresses.lib.etl_cli:main'],
    }
)
