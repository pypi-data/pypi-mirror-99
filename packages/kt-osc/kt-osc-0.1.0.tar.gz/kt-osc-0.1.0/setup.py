# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_osc']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['osc = kt_osc.cli:cli']}

setup_kwargs = {
    'name': 'kt-osc',
    'version': '0.1.0',
    'description': 'Calcula oscilacao de preco',
    'long_description': '# kt-osc\nFerramenta de linha de comando para calcular oscilação do preço em relação ao último fechamento.  \n\n## Instalação\npip install kt-osc\n\n## Uso\nosc preco-final preco-inicial  \n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-osc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
