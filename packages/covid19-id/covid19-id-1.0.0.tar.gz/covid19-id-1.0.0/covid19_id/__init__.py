from .version import __version__  # NOQA
from .update_covid19 import UpdateCovid19
from .provinsi import DataProvinsi
from .pemeriksaan_vaksinasi import PemeriksaanVaksinasi
from .data import Data
from .covid19_id import get_update, get_prov, get_pemeriksaan_vaksinasi, get_data


__author__ = "hexatester@protonmail.com"
__all__ = [
    "Data",
    "DataProvinsi",
    "PemeriksaanVaksinasi",
    "UpdateCovid19",
    "get_data",
    "get_pemeriksaan_vaksinasi",
    "get_prov",
    "get_update",
]
