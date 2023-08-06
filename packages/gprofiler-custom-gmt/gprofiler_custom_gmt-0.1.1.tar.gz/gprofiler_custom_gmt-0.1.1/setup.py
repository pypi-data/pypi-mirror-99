# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gprofiler_custom_gmt']

package_data = \
{'': ['*']}

install_requires = \
['gprofiler-official>=1.0.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['gprofiler_custom_gmt = gprofiler_custom_gmt.main:cli']}

setup_kwargs = {
    'name': 'gprofiler-custom-gmt',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Hugo Martiniano',
    'author_email': 'hugomartiniano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
