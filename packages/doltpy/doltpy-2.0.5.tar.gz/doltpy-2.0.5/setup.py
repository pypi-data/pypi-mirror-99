# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doltpy',
 'doltpy.cli',
 'doltpy.etl',
 'doltpy.shared',
 'doltpy.sql',
 'doltpy.sql.sync',
 'doltpy.types']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.3.18',
 'attrs==19.3.0',
 'decorator==4.4.2',
 'doltcli==0.1.2',
 'more-itertools>=8.6.0,<9.0.0',
 'mysql-connector-python>=8.0.20,<9.0.0',
 'numpy==1.19.0',
 'packaging==20.4',
 'pandas>=1.0.5',
 'pluggy==0.13.1',
 'protobuf==3.12.2',
 'psutil==5.7.2',
 'py==1.9.0',
 'pyparsing==2.4.7',
 'python-dateutil==2.8.1',
 'pytz==2020.1',
 'retry==0.9.2',
 'six==1.15.0',
 'wcwidth==0.2.5']

setup_kwargs = {
    'name': 'doltpy',
    'version': '2.0.5',
    'description': '',
    'long_description': None,
    'author': 'Oscar Batori',
    'author_email': 'oscar@dolthub.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
