from .version import __version__  # NOQA
from .update_covid19 import UpdateCovid19
from .provinsi import DataProvinsi
from .covid19_id import get_update, get_prov


__all__ = [
    "UpdateCovid19",
    "DataProvinsi",
    "get_update",
    "get_prov",
]
