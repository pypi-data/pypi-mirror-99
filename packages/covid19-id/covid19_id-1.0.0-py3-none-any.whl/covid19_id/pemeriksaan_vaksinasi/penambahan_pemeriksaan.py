import attr
from datetime import date, datetime


@attr.dataclass(slots=True)
class PenambahanPemeriksaan:
    jumlah_spesimen_pcr_tcm: int
    jumlah_spesimen_antigen: int
    jumlah_orang_pcr_tcm: int
    jumlah_orang_antigen: int
    tanggal: date
    created: datetime
