# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covid19_id', 'covid19_id.update']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'cattrs>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'covid19-id',
    'version': '0.1.0',
    'description': 'Python module for getting data from covid19.go.id',
    'long_description': '# covid19-id\n\n[![covid19-id - PyPi](https://img.shields.io/pypi/v/covid19-id)](https://pypi.org/project/covid19-id/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/covid19-id)](https://pypi.org/project/covid19-id/)\n[![LICENSE](https://img.shields.io/github/license/hexatester/covid19-id)](https://github.com/hexatester/covid19-id/blob/main/LICENSE)\n\nPython module for getting data from covid19.go.id\nModul python untuk mengambil data dari covid19.go.id\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexatester/covid19-id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
