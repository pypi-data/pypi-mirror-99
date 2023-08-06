# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covid19_id', 'covid19_id.update_covid19']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'cattrs>=1.3.0,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'covid19-id',
    'version': '0.2.0',
    'description': 'Python module for getting data from covid19.go.id',
    'long_description': '# covid19-id\n\n[![covid19-id - PyPi](https://img.shields.io/pypi/v/covid19-id)](https://pypi.org/project/covid19-id/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/covid19-id)](https://pypi.org/project/covid19-id/)\n[![LICENSE](https://img.shields.io/github/license/hexatester/covid19-id)](https://github.com/hexatester/covid19-id/blob/main/LICENSE)\n\nPython module for getting data from covid19.go.id\nModul python untuk mengambil data dari covid19.go.id\n\n## Install\n\nYou can install or upgrade covid19-id with:\n\n```bash\npip install covid19-id --upgrade\n```\n\n## Optional Dependencies\n\ncovid19-id can be installed with optional [ujson](https://pypi.org/project/ujson/ "ujson - PyPi") dependency.\n\n```bash\npip install covid19-id[ujson]`.\n```\n\nIt will then be used for JSON decoding, which can bring speed up compared to the standard [json](https://docs.python.org/3/library/json.html "python json docs") library.\n\n## Example\n\n```python\nimport covid19_id\n\nall_update = covid19_id.get_update()\n\ntotal = all_update.update.total\n\nprint(f"covid19; positive cases in Indonesia : {total.jumlah_positif}")\nprint(f"covid19; patients treated in Indonesia {total.jumlah_dirawat}")\nprint(f"covid19; patients recovered in Indonesia {total.jumlah_sembuh}")\nprint(f"covid19; patients died in Indonesia {total.jumlah_meninggal}")\n\n```\n',
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
