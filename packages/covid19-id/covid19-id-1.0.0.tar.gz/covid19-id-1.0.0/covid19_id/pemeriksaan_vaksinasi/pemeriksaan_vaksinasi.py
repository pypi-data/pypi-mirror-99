import attr

from . import Pemeriksaan
from . import Vaksinasi


@attr.dataclass(slots=True)
class PemeriksaanVaksinasi:
    pemeriksaan: Pemeriksaan
    vaksinasi: Vaksinasi
