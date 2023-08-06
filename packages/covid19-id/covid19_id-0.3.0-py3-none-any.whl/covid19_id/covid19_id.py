import cattr
from datetime import date, datetime
from dateutil.parser import parse as parse_datetime
from urllib.request import urlopen, Request

try:
    import ujson as json
except ImportError:
    import json  # type: ignore[no-redef]

from covid19_id.utils import ValueInt, get_headers
from . import UpdateCovid19
from . import DataProvinsi


def get_update(
    url: str = "https://data.covid19.go.id/public/api/update.json",
) -> UpdateCovid19:
    data: str = ""
    req = Request(url=url, headers=get_headers())
    cattr.register_structure_hook(date, lambda d, t: parse_datetime(d).date())
    cattr.register_structure_hook(datetime, lambda d, t: parse_datetime(d))
    cattr.register_structure_hook(ValueInt, lambda d, t: d["value"])
    with urlopen(req) as response:
        data = response.read()
    return cattr.structure(json.loads(data), UpdateCovid19)


def get_prov(
    url: str = "https://data.covid19.go.id/public/api/prov.json",
) -> DataProvinsi:
    data: str = ""
    req = Request(url=url, headers=get_headers())
    cattr.register_structure_hook(date, lambda d, t: parse_datetime(d).date())
    cattr.register_structure_hook(datetime, lambda d, t: parse_datetime(d))
    cattr.register_structure_hook(ValueInt, lambda d, t: d["value"])
    with urlopen(req) as response:
        data = response.read()
    return cattr.structure(json.loads(data), DataProvinsi)
