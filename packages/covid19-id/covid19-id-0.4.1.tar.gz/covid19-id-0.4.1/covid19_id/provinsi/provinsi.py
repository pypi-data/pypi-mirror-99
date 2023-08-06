import attr
from typing import List

from . import JenisKelamin, KelompokUmur, Lokasi, Penambahan


@attr.dataclass(slots=True)
class Provinsi:
    key: str
    doc_count: float
    jumlah_kasus: int
    jumlah_sembuh: int
    jumlah_meninggal: int
    jumlah_dirawat: int
    jenis_kelamin: List[JenisKelamin]
    kelompok_umur: List[KelompokUmur]
    lokasi: Lokasi
    penambahan: Penambahan
