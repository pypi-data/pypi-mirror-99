import attr
from datetime import date, datetime


@attr.dataclass(slots=True)
class PenambahanVaksinasi:
    jumlah_vaksinasi_1: int
    jumlah_vaksinasi_2: int
    tanggal: date
    created: datetime
