from .version import __version__  # NOQA
from .update_covid19 import UpdateCovid19
from .provinsi import DataProvinsi
from .pemeriksaan_vaksinasi import PemeriksaanVaksinasi
from .covid19_id import get_update, get_prov, get_pemeriksaan_vaksinasi


__all__ = [
    "UpdateCovid19",
    "DataProvinsi",
    "PemeriksaanVaksinasi",
    "get_update",
    "get_prov",
    "get_pemeriksaan_vaksinasi",
]
