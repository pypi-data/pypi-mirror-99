# covid19-id

[![covid19-id - PyPi](https://img.shields.io/pypi/v/covid19-id)](https://pypi.org/project/covid19-id/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/covid19-id)](https://pypi.org/project/covid19-id/)
[![LICENSE](https://img.shields.io/github/license/hexatester/covid19-id)](https://github.com/hexatester/covid19-id/blob/main/LICENSE)

Python module for getting data from covid19.go.id
Modul python untuk mengambil data dari covid19.go.id

## Install

You can install or upgrade covid19-id with:

```bash
pip install covid19-id --upgrade
```

## Optional Dependencies

covid19-id can be installed with optional [ujson](https://pypi.org/project/ujson/ "ujson - PyPi") dependency.

```bash
pip install covid19-id[ujson]`.
```

It will then be used for JSON decoding, which can bring speed up compared to the standard [json](https://docs.python.org/3/library/json.html "python json docs") library.

## Example

```python
import covid19_id

all_update = covid19_id.get_update()

total = all_update.update.total

print(f"covid19; positive cases in Indonesia : {total.jumlah_positif}")
print(f"covid19; patients treated in Indonesia {total.jumlah_dirawat}")
print(f"covid19; patients recovered in Indonesia {total.jumlah_sembuh}")
print(f"covid19; patients died in Indonesia {total.jumlah_meninggal}")

```
