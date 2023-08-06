import attr
from datetime import datetime
from dateutil.parser import parse
from typing import Optional

from covid19_id.utils import ValueInt


@attr.dataclass(slots=True)
class Harian:
    key_as_string: str
    key: int
    doc_count: int
    jumlah_meninggal: ValueInt
    jumlah_sembuh: ValueInt
    jumlah_positif: ValueInt
    jumlah_dirawat: ValueInt
    jumlah_positif_kum: ValueInt
    jumlah_sembuh_kum: ValueInt
    jumlah_meninggal_kum: ValueInt
    jumlah_dirawat_kum: ValueInt
    _datetime: Optional[datetime] = None

    @property
    def datetime(self) -> datetime:
        if self._datetime:
            return self._datetime
        self._datetime = parse(self.key_as_string)
        return self._datetime
