import attr
from typing import List

from . import PenambahanPemeriksaan
from . import PemeriksaanHarian
from . import TotalPemeriksaan


@attr.dataclass(slots=True)
class Pemeriksaan:
    penambahan: PenambahanPemeriksaan
    harian: List[PemeriksaanHarian]
    total: TotalPemeriksaan
