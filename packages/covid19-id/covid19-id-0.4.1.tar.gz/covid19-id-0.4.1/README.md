# covid19-id

[![covid19-id - PyPi](https://img.shields.io/pypi/v/covid19-id)](https://pypi.org/project/covid19-id/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/covid19-id)](https://pypi.org/project/covid19-id/)
[![LICENSE](https://img.shields.io/github/license/hexatester/covid19-id)](https://github.com/hexatester/covid19-id/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/hexatester/covid19-id/branch/main/graph/badge.svg)](https://codecov.io/gh/hexatester/covid19-id)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)

Python module for getting data from covid19.go.id

[Readme Bahasa Indonesia](README.id.md)

## Install

You can install or upgrade covid19-id with:

```bash
pip install covid19-id --upgrade
```

## Optional Dependencies

covid19-id can be installed with optional [ujson](https://pypi.org/project/ujson/ "ujson - PyPi") dependency.

```bash
pip install covid19-id[ujson]
```

It will then be used for JSON decoding, which can bring speed up compared to the standard [json](https://docs.python.org/3/library/json.html "python json docs") library.

## Example

### Get Updates

```python
import covid19_id

all_update = covid19_id.get_update()

total = all_update.update.total

print(f"covid19; positive cases in Indonesia : {total.jumlah_positif}")
print(f"covid19; patients treated in Indonesia {total.jumlah_dirawat}")
print(f"covid19; patients recovered in Indonesia {total.jumlah_sembuh}")
print(f"covid19; patients died in Indonesia {total.jumlah_meninggal}")

```

### Provinsi

```python
import covid19_id

data_provinsi = covid19_id.get_prov()

for provinsi in data_provinsi.list_data:
    print(f"Province : {provinsi.key}")
    print(f"Cases {provinsi.jumlah_kasus}")
    print(f"Recovered {provinsi.jumlah_sembuh}")
    print(f"Died {provinsi.jumlah_meninggal}")
    for umur in provinsi.kelompok_umur:
        print(f"Age {umur.key} : {umur.doc_count}")
    penambahan = provinsi.penambahan
    print(f"Additional Positive Cases {penambahan.positif}")
    print(f"Additional Recovered {penambahan.sembuh}")
    print(f"Additional Died {penambahan.meninggal}")
    print("")

```

### Vaccinated

```python
import covid19_id


pemeriksaan_vaksinasi = covid19_id.get_pemeriksaan_vaksinasi()

vaksinasi_total = pemeriksaan_vaksinasi.vaksinasi.total

print(f"vaccinated population (first one) {vaksinasi_total.jumlah_vaksinasi_1}")
print(f"vaccinated population (second time) {vaksinasi_total.jumlah_vaksinasi_2}")

```
