# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_otm']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['otm = kt_otm.cli:cli']}

setup_kwargs = {
    'name': 'kt-otm',
    'version': '0.1.0',
    'description': 'Calcula os strikes fora do dinheiro',
    'long_description': '# kt-otm\nCalcula os strikes fora do dinheiro\n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-otm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
