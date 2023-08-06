import attr
from datetime import datetime, date

from covid19_id.utils import str_to_date, str_to_datetime


@attr.dataclass(slots=True)
class Penambahan:
    jumlah_positif: int
    jumlah_meninggal: int
    jumlah_sembuh: int
    jumlah_dirawat: int
    tanggal: date = attr.ib(converter=str_to_date)
    created: datetime = attr.ib(converter=str_to_datetime)
