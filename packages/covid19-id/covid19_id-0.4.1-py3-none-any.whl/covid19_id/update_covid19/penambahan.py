import attr
from datetime import datetime, date


@attr.dataclass(slots=True)
class Penambahan:
    jumlah_positif: int
    jumlah_meninggal: int
    jumlah_sembuh: int
    jumlah_dirawat: int
    tanggal: date
    created: datetime
