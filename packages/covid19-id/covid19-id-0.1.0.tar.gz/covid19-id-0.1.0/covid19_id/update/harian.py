import attr
from datetime import datetime


@attr.dataclass(slots=True)
class HarianValue:
    value: int

    def __get__(self, instance, owner):
        return self.value


@attr.dataclass(slots=True)
class Harian:
    key_as_string: str
    key: int
    doc_count: int
    jumlah_meninggal: int = attr.ib(converter=HarianValue)
    jumlah_sembuh: int = attr.ib(converter=HarianValue)
    jumlah_positif: int = attr.ib(converter=HarianValue)
    jumlah_dirawat: int = attr.ib(converter=HarianValue)
    jumlah_positif_kum: int = attr.ib(converter=HarianValue)
    jumlah_sembuh_kum: int = attr.ib(converter=HarianValue)
    jumlah_meninggal_kum: int = attr.ib(converter=HarianValue)
    jumlah_dirawat_kum: int = attr.ib(converter=HarianValue)

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.key)
