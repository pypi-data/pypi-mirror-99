import cattr
from datetime import date, datetime
from dateutil.parser import parse as parse_datetime
from urllib.request import urlopen, Request

try:
    import ujson as json
except ImportError:
    import json  # type: ignore[no-redef]

from covid19_id.utils import ValueInt
from . import UpdateCovid19
from . import __version__


def get_update(
    url: str = "https://data.covid19.go.id/public/api/update.json",
) -> UpdateCovid19:
    data: str = ""
    headers = {"User-Agent": f"pypi.org/project/covid19-id/{__version__}"}
    req = Request(url=url, headers=headers)
    cattr.register_structure_hook(date, lambda d, t: parse_datetime(d).date())
    cattr.register_structure_hook(datetime, lambda d, t: parse_datetime(d))
    cattr.register_structure_hook(ValueInt, lambda d, t: d["value"])
    with urlopen(req) as response:
        data = response.read()
    return cattr.structure(json.loads(data), UpdateCovid19)
