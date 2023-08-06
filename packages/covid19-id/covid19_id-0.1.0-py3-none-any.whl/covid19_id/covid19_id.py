import attr
from cattr import structure
from urllib.request import urlopen, Request

try:
    import ujson as json
except ImportError:
    import json

from . import Data
from . import Update
from . import __version__


def get_update(
    url: str = "https://data.covid19.go.id/public/api/update.json",
) -> Update:
    data: str = ""
    headers = {"User-Agent": f"pypi.org/project/covid19-id/{__version__}"}
    req = Request(url=url, headers=headers)
    with urlopen(req) as response:
        data = response.read()
    return structure(json.loads(data), Update)


@attr.dataclass(slots=True)
class Covid19ID:
    data: Data
    update: Update
