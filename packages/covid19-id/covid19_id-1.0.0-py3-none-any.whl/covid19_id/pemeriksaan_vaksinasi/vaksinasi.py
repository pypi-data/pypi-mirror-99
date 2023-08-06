import attr
from typing import List

from . import PenambahanVaksinasi
from . import VaksinasiHarian
from . import TotalVaksinasi


@attr.dataclass(slots=True)
class Vaksinasi:
    penambahan: PenambahanVaksinasi
    harian: List[VaksinasiHarian]
    total: TotalVaksinasi
