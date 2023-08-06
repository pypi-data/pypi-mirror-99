# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_pullback']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['pb = kt_pullback.cli:cli']}

setup_kwargs = {
    'name': 'kt-pullback',
    'version': '0.1.0',
    'description': '',
    'long_description': '# kt-pullback\nCalcula os preços de retração de uma pernada no gráfico\n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-pullback',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
