# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_powerbi_metadata']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pytz==2018.4',
 'singer-python==5.9.0',
 'singer-sdk==0.0.2.dev1074572064']

entry_points = \
{'console_scripts': ['tap-powerbi-metadata = tap_powerbi_metadata.tap:cli']}

setup_kwargs = {
    'name': 'tap-powerbi-metadata',
    'version': '0.0.1',
    'description': '`tap-powerbi-metadata` is Singer-compliant PowerBIMetadata tap built with Singer SDK.',
    'long_description': None,
    'author': 'AJ Steers',
    'author_email': 'aaaronsteers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
