# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covid19_id',
 'covid19_id.pemeriksaan_vaksinasi',
 'covid19_id.provinsi',
 'covid19_id.update_covid19']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'cattrs>=1.3.0,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

extras_require = \
{'ujson': ['ujson>=4.0.2,<5.0.0']}

setup_kwargs = {
    'name': 'covid19-id',
    'version': '0.4.1',
    'description': 'Python module for getting data from covid19.go.id',
    'long_description': '# covid19-id\n\n[![covid19-id - PyPi](https://img.shields.io/pypi/v/covid19-id)](https://pypi.org/project/covid19-id/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/covid19-id)](https://pypi.org/project/covid19-id/)\n[![LICENSE](https://img.shields.io/github/license/hexatester/covid19-id)](https://github.com/hexatester/covid19-id/blob/main/LICENSE)\n[![codecov](https://codecov.io/gh/hexatester/covid19-id/branch/main/graph/badge.svg)](https://codecov.io/gh/hexatester/covid19-id)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)\n\nPython module for getting data from covid19.go.id\n\n[Readme Bahasa Indonesia](README.id.md)\n\n## Install\n\nYou can install or upgrade covid19-id with:\n\n```bash\npip install covid19-id --upgrade\n```\n\n## Optional Dependencies\n\ncovid19-id can be installed with optional [ujson](https://pypi.org/project/ujson/ "ujson - PyPi") dependency.\n\n```bash\npip install covid19-id[ujson]\n```\n\nIt will then be used for JSON decoding, which can bring speed up compared to the standard [json](https://docs.python.org/3/library/json.html "python json docs") library.\n\n## Example\n\n### Get Updates\n\n```python\nimport covid19_id\n\nall_update = covid19_id.get_update()\n\ntotal = all_update.update.total\n\nprint(f"covid19; positive cases in Indonesia : {total.jumlah_positif}")\nprint(f"covid19; patients treated in Indonesia {total.jumlah_dirawat}")\nprint(f"covid19; patients recovered in Indonesia {total.jumlah_sembuh}")\nprint(f"covid19; patients died in Indonesia {total.jumlah_meninggal}")\n\n```\n\n### Provinsi\n\n```python\nimport covid19_id\n\ndata_provinsi = covid19_id.get_prov()\n\nfor provinsi in data_provinsi.list_data:\n    print(f"Province : {provinsi.key}")\n    print(f"Cases {provinsi.jumlah_kasus}")\n    print(f"Recovered {provinsi.jumlah_sembuh}")\n    print(f"Died {provinsi.jumlah_meninggal}")\n    for umur in provinsi.kelompok_umur:\n        print(f"Age {umur.key} : {umur.doc_count}")\n    penambahan = provinsi.penambahan\n    print(f"Additional Positive Cases {penambahan.positif}")\n    print(f"Additional Recovered {penambahan.sembuh}")\n    print(f"Additional Died {penambahan.meninggal}")\n    print("")\n\n```\n\n### Vaccinated\n\n```python\nimport covid19_id\n\n\npemeriksaan_vaksinasi = covid19_id.get_pemeriksaan_vaksinasi()\n\nvaksinasi_total = pemeriksaan_vaksinasi.vaksinasi.total\n\nprint(f"vaccinated population (first one) {vaksinasi_total.jumlah_vaksinasi_1}")\nprint(f"vaccinated population (second time) {vaksinasi_total.jumlah_vaksinasi_2}")\n\n```\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexatester/covid19-id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
