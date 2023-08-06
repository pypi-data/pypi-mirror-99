import cattr
from datetime import date, datetime
from dateutil.parser import parse as parse_datetime
from typing import Any
from urllib.request import urlopen, Request

try:
    import ujson as json
except ImportError:
    import json  # type: ignore[no-redef]

from covid19_id.utils import ValueInt, get_headers
from . import UpdateCovid19
from . import DataProvinsi
from . import PemeriksaanVaksinasi


def _get_data(url: str, to_json: bool = True) -> Any:
    data: Any = None
    req = Request(url=url, headers=get_headers())
    with urlopen(req) as response:
        data = response.read()
    if to_json:
        return json.loads(data)
    return data


def get_update(
    url: str = "https://data.covid19.go.id/public/api/update.json",
) -> UpdateCovid19:
    cattr.register_structure_hook(date, lambda d, t: parse_datetime(d).date())
    cattr.register_structure_hook(datetime, lambda d, t: parse_datetime(d))
    cattr.register_structure_hook(ValueInt, lambda d, t: d["value"])
    data = _get_data(url)
    return cattr.structure(data, UpdateCovid19)


def get_prov(
    url: str = "https://data.covid19.go.id/public/api/prov.json",
) -> DataProvinsi:
    cattr.register_structure_hook(date, lambda d, t: parse_datetime(d).date())
    cattr.register_structure_hook(datetime, lambda d, t: parse_datetime(d))
    cattr.register_structure_hook(ValueInt, lambda d, t: d["value"])
    data = _get_data(url)
    return cattr.structure(data, DataProvinsi)


def get_pemeriksaan_vaksinasi(
    url: str = "https://data.covid19.go.id/public/api/pemeriksaan-vaksinasi.json",
) -> PemeriksaanVaksinasi:
    cattr.register_structure_hook(date, lambda d, t: parse_datetime(d).date())
    cattr.register_structure_hook(datetime, lambda d, t: parse_datetime(d))
    cattr.register_structure_hook(ValueInt, lambda d, t: d["value"])
    data = _get_data(url)
    return cattr.structure(data, PemeriksaanVaksinasi)
