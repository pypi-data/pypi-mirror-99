# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dcm_metrics']

package_data = \
{'': ['*']}

install_requires = \
['opencensus-ext-azure>=1.0.7,<2.0.0', 'opencensus>=0.7.12,<0.8.0']

setup_kwargs = {
    'name': 'dcm-metrics',
    'version': '0.1.0',
    'description': 'Package for sending metrics to Azure Application Insights',
    'long_description': None,
    'author': 'Jan Lukány',
    'author_email': 'lukany.jan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
